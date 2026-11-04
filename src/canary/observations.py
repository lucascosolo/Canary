"""Indicators and observations with vintages. Nothing here commits."""

from __future__ import annotations

import datetime
import hashlib
import json
import math
import uuid
from collections.abc import Sequence
from dataclasses import asdict, dataclass
from typing import Any

from sqlalchemy import insert, select, text, update
from sqlalchemy.orm import Session

from canary.ids import new_id
from canary.schema import dataset_release, indicator, indicator_version, observation

DIRECTIONS = ("up", "down", "none")
CHUNK = 20_000
COUNTED_TABLES = (
    "baseline",
    "dataset_release",
    "indicator",
    "indicator_version",
    "observation",
    "pipeline_run",
    "place",
    "place_version",
    "source",
    "source_health",
    "source_version",
)


@dataclass(frozen=True)
class IndicatorSpec:
    id: str
    source_id: str
    name: str
    definition: str
    domain: str
    unit: str
    cadence: str
    deterioration_direction: str
    reporting_bias_note: str

    def __post_init__(self) -> None:
        if self.deterioration_direction not in DIRECTIONS:
            raise ValueError(f"deterioration_direction must be one of {DIRECTIONS}")


def sync_indicator(session: Session, spec: IndicatorSpec, *, run_id: uuid.UUID) -> int:
    record = asdict(spec)
    digest = hashlib.sha256(
        json.dumps(record, sort_keys=True, separators=(",", ":")).encode("utf-8")
    ).hexdigest()
    known = session.execute(
        select(indicator.c.current_version, indicator_version.c.digest).join(
            indicator_version,
            (indicator_version.c.indicator_id == indicator.c.id)
            & (indicator_version.c.version == indicator.c.current_version),
        )
        .where(indicator.c.id == spec.id)
    ).one_or_none()
    if known is not None and known.digest == digest:
        return known.current_version
    version = 1 if known is None else known.current_version + 1
    if known is None:
        session.execute(
            insert(indicator).values(
                id=spec.id, current_version=version, source_id=spec.source_id, record=record
            )
        )
    else:
        session.execute(
            update(indicator)
            .where(indicator.c.id == spec.id)
            .values(current_version=version, source_id=spec.source_id, record=record)
        )
    session.execute(
        insert(indicator_version).values(
            indicator_id=spec.id,
            version=version,
            record=record,
            digest=digest,
            recorded_at=datetime.datetime.now(datetime.UTC),
            run_id=run_id,
        )
    )
    return version


@dataclass(frozen=True)
class ObservationRow:
    indicator_id: str
    geo_ref: str
    period_start: datetime.date
    period_end: datetime.date
    value: float
    value_low: float | None = None
    value_high: float | None = None


@dataclass(frozen=True)
class StoredObservation(ObservationRow):
    vintage_release_id: uuid.UUID | None = None
    retrieved_at: datetime.datetime | None = None
    run_id: uuid.UUID | None = None


@dataclass(frozen=True)
class WriteResult:
    written: int
    unchanged: int


def _key(row: ObservationRow) -> tuple[str, str, datetime.date, datetime.date]:
    return (row.indicator_id, row.geo_ref, row.period_start, row.period_end)


def _values(row: ObservationRow) -> tuple[float, float | None, float | None]:
    return (row.value, row.value_low, row.value_high)


def _validate(rows: Sequence[ObservationRow]) -> None:
    seen: set[tuple[str, str, datetime.date, datetime.date]] = set()
    for row in rows:
        for number in _values(row):
            if number is not None and not math.isfinite(number):
                raise ValueError(f"non-finite value for {_key(row)}")
        key = _key(row)
        if key in seen:
            raise ValueError(f"duplicate key in one call: {key}")
        seen.add(key)


def _ensure_partition(session: Session, retrieved_at: datetime.datetime) -> None:
    moment = retrieved_at.astimezone(datetime.UTC)
    first = datetime.date(moment.year, moment.month, 1)
    following = datetime.date(moment.year + moment.month // 12, moment.month % 12 + 1, 1)
    name = f"observation_{first.year:04d}_{first.month:02d}"
    session.execute(
        text(
            f"create table if not exists {name} partition of observation "
            f"for values from ('{first.isoformat()} 00:00:00+00') "
            f"to ('{following.isoformat()} 00:00:00+00')"
        )
    )
    create = f"create or replace trigger {name}_nt before truncate on {name} "  # SAFETY-GUARD
    session.execute(text(create + "for each statement execute function canary_refuse()"))


LATEST_SQL = text(
    """
    select distinct on (o.indicator_id, o.geo_ref, o.period_start, o.period_end)
        o.indicator_id, o.geo_ref, o.period_start, o.period_end,
        o.value, o.value_low, o.value_high
    from observation o
    join unnest(
        cast(:ind as text[]), cast(:geo as text[]), cast(:ps as date[]), cast(:pe as date[])
    ) as k(indicator_id, geo_ref, period_start, period_end)
      on o.indicator_id = k.indicator_id and o.geo_ref = k.geo_ref
     and o.period_start = k.period_start and o.period_end = k.period_end
    order by o.indicator_id, o.geo_ref, o.period_start, o.period_end, o.retrieved_at desc, o.id desc
    """
)


def _latest_values(
    session: Session, rows: Sequence[ObservationRow]
) -> dict[Any, tuple[float, float | None, float | None]]:
    latest: dict[Any, tuple[float, float | None, float | None]] = {}
    for start in range(0, len(rows), CHUNK):
        chunk = rows[start : start + CHUNK]
        result = session.execute(
            LATEST_SQL,
            {
                "ind": [r.indicator_id for r in chunk],
                "geo": [r.geo_ref for r in chunk],
                "ps": [r.period_start for r in chunk],
                "pe": [r.period_end for r in chunk],
            },
        )
        for found in result:
            latest[tuple(found[:4])] = (found[4], found[5], found[6])
    return latest


def write_observations(
    session: Session,
    release_id: uuid.UUID,
    run_id: uuid.UUID,
    rows: Sequence[ObservationRow],
    *,
    at: datetime.datetime | None = None,
) -> WriteResult:
    """Write the rows that differ from each key's newest vintage, stamped `at` or the release."""
    _validate(rows)
    retrieved_at = at or session.execute(
        select(dataset_release.c.retrieved_at).where(dataset_release.c.id == release_id)
    ).scalar_one()
    _ensure_partition(session, retrieved_at)
    latest = _latest_values(session, rows)
    fresh = [r for r in rows if latest.get(_key(r)) != _values(r)]
    for start in range(0, len(fresh), CHUNK):
        session.execute(
            insert(observation),
            [
                {
                    "id": new_id(),
                    "indicator_id": r.indicator_id,
                    "geo_ref": r.geo_ref,
                    "period_start": r.period_start,
                    "period_end": r.period_end,
                    "value": r.value,
                    "value_low": r.value_low,
                    "value_high": r.value_high,
                    "vintage_release_id": release_id,
                    "retrieved_at": retrieved_at,
                    "run_id": run_id,
                }
                for r in fresh[start : start + CHUNK]
            ],
        )
    return WriteResult(written=len(fresh), unchanged=len(rows) - len(fresh))


AS_OF_SQL = text(
    """
    select * from (
        select distinct on (indicator_id, geo_ref, period_start, period_end)
            indicator_id, geo_ref, period_start, period_end, value, value_low, value_high,
            vintage_release_id, retrieved_at, run_id
        from observation
        where indicator_id = :indicator_id
          and (cast(:as_of as timestamptz) is null or retrieved_at <= cast(:as_of as timestamptz))
          and (cast(:geo_ref as text) is null or geo_ref = cast(:geo_ref as text))
        order by indicator_id, geo_ref, period_start, period_end, retrieved_at desc, id desc
    ) latest
    order by geo_ref, period_start, period_end
    """
)


def _as_of(
    session: Session, indicator_id: str, as_of: datetime.datetime | None, geo_ref: str | None
) -> list[StoredObservation]:
    result = session.execute(
        AS_OF_SQL, {"indicator_id": indicator_id, "as_of": as_of, "geo_ref": geo_ref}
    )
    return [StoredObservation(*found) for found in result]


def observations_as_of(
    session: Session, indicator_id: str, as_of: datetime.datetime, *, geo_ref: str | None = None
) -> list[StoredObservation]:
    return _as_of(session, indicator_id, as_of, geo_ref)


def observation_digest(
    session: Session, source_id: str, as_of: datetime.datetime | None = None
) -> str:
    ids = session.execute(
        select(indicator.c.id).where(indicator.c.source_id == source_id).order_by(indicator.c.id)
    ).scalars()
    digest = hashlib.sha256()
    for indicator_id in ids:
        for o in _as_of(session, indicator_id, as_of, None):
            parts = [
                indicator_id,
                o.geo_ref,
                o.period_start.isoformat(),
                o.period_end.isoformat(),
                repr(o.value),
                "null" if o.value_low is None else repr(o.value_low),
                "null" if o.value_high is None else repr(o.value_high),
            ]
            digest.update(("|".join(parts) + "\n").encode("utf-8"))
    return digest.hexdigest()


def table_counts(session: Session) -> dict[str, int]:
    return {
        table: session.execute(text(f"select count(*) from {table}")).scalar_one()
        for table in COUNTED_TABLES
    }
