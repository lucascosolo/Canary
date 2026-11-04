"""Provenance spine: runs, registry sync, releases and source health. Nothing here commits."""

from __future__ import annotations

import datetime
import hashlib
import json
import uuid
from collections.abc import Sequence
from dataclasses import dataclass
from typing import Any

from sqlalchemy import func, insert, select, update
from sqlalchemy.dialects.postgresql import insert as pg_insert
from sqlalchemy.orm import Session

from canary.ids import new_id
from canary.registry import SourceEntry
from canary.schema import (
    dataset_release,
    pipeline_run,
    source,
    source_health,
    source_version,
)

VERSION_FIELDS = frozenset(
    {
        "model_id",
        "prompt_version",
        "schema_version",
        "indicator_catalog_version",
        "rule_file_version",
        "notes",
    }
)


def _now() -> datetime.datetime:
    return datetime.datetime.now(datetime.UTC)


def start_run(
    session: Session,
    stage: str,
    *,
    code_commit: str,
    config_digest: str,
    started_at: datetime.datetime | None = None,
    **versions: str | None,
) -> uuid.UUID:
    unknown = set(versions) - VERSION_FIELDS
    if unknown:
        raise TypeError(f"unexpected keyword arguments: {', '.join(sorted(unknown))}")
    run_id = new_id()
    session.execute(
        insert(pipeline_run).values(
            id=run_id,
            stage=stage,
            started_at=started_at or _now(),
            code_commit=code_commit,
            config_digest=config_digest,
            **versions,
        )
    )
    return run_id


def finish_run(
    session: Session,
    run_id: uuid.UUID,
    *,
    input_count: int = 0,
    output_count: int = 0,
    error_count: int = 0,
    notes: str | None = None,
    ended_at: datetime.datetime | None = None,
) -> None:
    session.execute(
        update(pipeline_run)
        .where(pipeline_run.c.id == run_id)
        .values(
            ended_at=ended_at or _now(),
            input_count=input_count,
            output_count=output_count,
            error_count=error_count,
            notes=notes,
        )
    )


@dataclass(frozen=True)
class SyncResult:
    added: list[str]
    changed: list[str]
    unchanged: list[str]
    missing: list[str]


def entry_record(entry: SourceEntry) -> dict[str, Any]:
    return entry.model_dump(mode="json")


def entry_digest(entry: SourceEntry) -> str:
    text = json.dumps(entry_record(entry), sort_keys=True, separators=(",", ":"))
    return hashlib.sha256(text.encode("utf-8")).hexdigest()


def sync_registry(
    session: Session, entries: Sequence[SourceEntry], *, run_id: uuid.UUID
) -> SyncResult:
    current = {
        row.id: row
        for row in session.execute(
            select(source.c.id, source.c.current_version, source_version.c.digest).join(
                source_version,
                (source_version.c.source_id == source.c.id)
                & (source_version.c.version == source.c.current_version),
            )
        )
    }
    added: list[str] = []
    changed: list[str] = []
    unchanged: list[str] = []
    for entry in entries:
        digest = entry_digest(entry)
        record = entry_record(entry)
        known = current.get(entry.id)
        if known is not None and known.digest == digest:
            unchanged.append(entry.id)
            continue
        version = 1 if known is None else known.current_version + 1
        fields = {"canary_use": entry.canary_use, "status": entry.status, "record": record}
        if known is None:
            session.execute(insert(source).values(id=entry.id, current_version=version, **fields))
            added.append(entry.id)
        else:
            session.execute(
                update(source)
                .where(source.c.id == entry.id)
                .values(current_version=version, **fields)
            )
            changed.append(entry.id)
        session.execute(
            insert(source_version).values(
                source_id=entry.id,
                version=version,
                record=record,
                digest=digest,
                run_id=run_id,
                recorded_at=_now(),
            )
        )
    given = {entry.id for entry in entries}
    return SyncResult(
        added=sorted(added),
        changed=sorted(changed),
        unchanged=sorted(unchanged),
        missing=sorted(set(current) - given),
    )


def record_health(
    session: Session,
    source_id: str,
    *,
    ok: bool,
    latency_ms: int | None = None,
    items_seen: int | None = None,
    schema_digest: str | None = None,
    message: str | None = None,
    checked_at: datetime.datetime | None = None,
) -> uuid.UUID:
    health_id = new_id()
    session.execute(
        insert(source_health).values(
            id=health_id,
            source_id=source_id,
            checked_at=checked_at or _now(),
            ok=ok,
            latency_ms=latency_ms,
            items_seen=items_seen,
            schema_digest=schema_digest,
            message=message,
        )
    )
    return health_id


def record_release(
    session: Session,
    source_id: str,
    *,
    version_label: str,
    content_digest: str,
    row_count: int,
    schema_digest: str,
    licence_snapshot: str,
    file_refs: Any,
    run_id: uuid.UUID,
    retrieved_at: datetime.datetime | None = None,
    released_at: datetime.datetime | None = None,
) -> tuple[uuid.UUID, bool]:
    release_id = new_id()
    inserted = session.execute(
        pg_insert(dataset_release)
        .values(
            id=release_id,
            source_id=source_id,
            version_label=version_label,
            released_at=released_at,
            retrieved_at=retrieved_at or _now(),
            file_refs=file_refs,
            content_digest=content_digest,
            row_count=row_count,
            schema_digest=schema_digest,
            licence_snapshot=licence_snapshot,
            run_id=run_id,
        )
        .on_conflict_do_nothing(constraint="dataset_release_source_digest_key")
        .returning(dataset_release.c.id)
    ).scalar_one_or_none()
    if inserted is not None:
        return inserted, True
    existing = session.execute(
        select(dataset_release.c.id).where(
            dataset_release.c.source_id == source_id,
            dataset_release.c.content_digest == content_digest,
        )
    ).scalar_one()
    return existing, False


@dataclass(frozen=True)
class SourceHealth:
    source_id: str
    status: str
    canary_use: str
    last_ok_at: datetime.datetime | None
    last_failure_at: datetime.datetime | None
    expected_lag_days: int | None
    freshness: str


def _latest(*values: datetime.datetime | None) -> datetime.datetime | None:
    present = [v for v in values if v is not None]
    return max(present) if present else None


def _pairs(result: Any) -> dict[str, datetime.datetime]:
    return {row[0]: row[1] for row in result}


def health_report(session: Session, now: datetime.datetime | None = None) -> list[SourceHealth]:
    now = now or _now()
    ok_checks = _pairs(
        session.execute(
            select(source_health.c.source_id, func.max(source_health.c.checked_at))
            .where(source_health.c.ok)
            .group_by(source_health.c.source_id)
        )
    )
    failures = _pairs(
        session.execute(
            select(source_health.c.source_id, func.max(source_health.c.checked_at))
            .where(~source_health.c.ok)
            .group_by(source_health.c.source_id)
        )
    )
    retrievals = _pairs(
        session.execute(
            select(dataset_release.c.source_id, func.max(dataset_release.c.retrieved_at)).group_by(
                dataset_release.c.source_id
            )
        )
    )
    report: list[SourceHealth] = []
    for row in session.execute(
        select(source.c.id, source.c.status, source.c.canary_use, source.c.record).order_by(
            source.c.id
        )
    ):
        last_ok = _latest(ok_checks.get(row.id), retrievals.get(row.id))
        lag = row.record.get("expected_lag_days")
        if last_ok is None:
            freshness = "never_fetched"
        elif lag is None:
            freshness = "unknown"
        elif now - last_ok > datetime.timedelta(days=lag):
            freshness = "stale"
        else:
            freshness = "fresh"
        report.append(
            SourceHealth(
                source_id=row.id,
                status=row.status,
                canary_use=row.canary_use,
                last_ok_at=last_ok,
                last_failure_at=failures.get(row.id),
                expected_lag_days=lag,
                freshness=freshness,
            )
        )
    return report
