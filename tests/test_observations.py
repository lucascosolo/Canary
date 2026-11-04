"""Observations with vintages: indicators, append-only writes, as-of reads, digest and CLI."""

from __future__ import annotations

import datetime
import uuid
from collections.abc import Callable, Iterator
from typing import Any

import pytest
import sqlalchemy.exc
from alembic import command
from alembic.config import Config
from sqlalchemy import Engine, create_engine, text
from sqlalchemy.engine import make_url
from sqlalchemy.orm import Session

from canary.cli import main
from canary.observations import (
    IndicatorSpec,
    ObservationRow,
    observation_digest,
    observations_as_of,
    sync_indicator,
    table_counts,
    write_observations,
)
from canary.provenance import record_release, start_run, sync_registry
from canary.registry import SourceEntry

UTC = datetime.UTC
T1 = datetime.datetime(2026, 1, 10, 12, 0, tzinfo=UTC)
T2 = datetime.datetime(2026, 2, 10, 12, 0, tzinfo=UTC)
T3 = datetime.datetime(2026, 3, 10, 12, 0, tzinfo=UTC)
JAN = datetime.date(2026, 1, 1)
JAN_END = datetime.date(2026, 1, 31)
FEB = datetime.date(2026, 2, 1)
FEB_END = datetime.date(2026, 2, 28)
TABLES = [
    "baseline",
    "dataset_release",
    "indicator",
    "indicator_version",
    "observation",
    "pipeline_run",
    "place",
    "source",
    "source_health",
    "source_version",
]


def make_entry(source_id: str) -> SourceEntry:
    data: dict[str, Any] = {
        "id": source_id,
        "name": "Example Source",
        "organisation": "Example Org",
        "homepage": "https://example.org",
        "type": "api",
        "domains": ["economy"],
        "countries": "global",
        "languages": ["en"],
        "declared_cadence": "daily",
        "revision_policy": "none",
        "access_method": "REST",
        "auth": "none",
        "licence_id": "CC-BY-4.0",
        "terms_url": "https://example.org/terms",
        "terms_verified_on": datetime.date(2026, 11, 1),
        "canary_use": "open",
        "attribution_text": "Example Org",
        "source_class": "intergovernmental",
        "status": "lead",
    }
    return SourceEntry.model_validate(data, context={"today": datetime.date(2026, 11, 4)})


def spec(indicator_id: str = "ind-a", source_id: str = "obs-src", **overrides: Any) -> Any:
    args: dict[str, Any] = {
        "id": indicator_id,
        "source_id": source_id,
        "name": "Example indicator",
        "definition": "A thing measured",
        "domain": "economy",
        "unit": "percent",
        "cadence": "monthly",
        "deterioration_direction": "up",
        "reporting_bias_note": "none known",
    }
    args.update(overrides)
    return IndicatorSpec(**args)


def row(
    geo: str = "USA",
    start: datetime.date = JAN,
    end: datetime.date = JAN_END,
    value: float = 1.0,
    indicator_id: str = "ind-a",
    **kw: Any,
) -> Any:
    return ObservationRow(indicator_id, geo, start, end, value, **kw)


def new_run(session: Session) -> uuid.UUID:
    return start_run(session, "indicator", code_commit="abc123", config_digest="cfg")


def release(
    session: Session, source_id: str, run_id: uuid.UUID, retrieved_at: datetime.datetime, n: int = 0
) -> uuid.UUID:
    release_id, written = record_release(
        session,
        source_id,
        version_label="v",
        content_digest=f"digest-{source_id}-{retrieved_at.isoformat()}-{n}",
        row_count=1,
        schema_digest="s",
        licence_snapshot="CC-BY-4.0",
        file_refs={"files": []},
        run_id=run_id,
        retrieved_at=retrieved_at,
    )
    assert written
    return release_id


def setup_source(session: Session, source_id: str = "obs-src", *indicators: str) -> uuid.UUID:
    """A source and its indicators (default ind-a); returns an open run id."""
    run_id = new_run(session)
    sync_registry(session, [make_entry(source_id)], run_id=run_id)
    for indicator_id in indicators or ("ind-a",):
        sync_indicator(session, spec(indicator_id, source_id))
    return run_id


def load(
    session: Session,
    run_id: uuid.UUID,
    retrieved_at: datetime.datetime,
    rows: list[Any],
    source_id: str = "obs-src",
) -> Any:
    release_id = release(session, source_id, run_id, retrieved_at)
    return write_observations(session, release_id, run_id, rows)


def scalar(session: Session, sql: str, **params: Any) -> Any:
    return session.execute(text(sql), params).scalar_one()


def count(session: Session, table: str) -> int:
    return scalar(session, f"select count(*) from {table}")


def refused(session: Session, sql: str, **params: Any) -> None:
    with pytest.raises(sqlalchemy.exc.DBAPIError):
        with session.begin_nested():
            session.execute(text(sql), params)


def insert_observation(session: Session, run_id: uuid.UUID, start: Any, end: Any) -> None:
    session.execute(
        text(
            "insert into observation (id, indicator_id, geo_ref, period_start, period_end, value, "
            "vintage_release_id, retrieved_at, run_id) "
            "select :id, 'ind-a', 'USA', :s, :e, 1.0, id, retrieved_at, :r "
            "from dataset_release order by retrieved_at limit 1"
        ),
        {"id": uuid.uuid4(), "s": start, "e": end, "r": run_id},
    )


def insert_baseline(session: Session, run_id: uuid.UUID, horizon: str = "12m") -> None:
    session.execute(
        text(
            "insert into baseline (id, indicator_id, geo_ref, horizon, computed_at, stats, "
            "method_version, run_id) values (:id, 'ind-a', 'USA', :h, now(), '{}', 'm1', :r)"
        ),
        {"id": uuid.uuid4(), "h": horizon, "r": run_id},
    )


@pytest.fixture
def loaded(db_session: Session) -> uuid.UUID:
    """One source, one indicator, one release with one observation, one baseline."""
    run_id = setup_source(db_session)
    load(db_session, run_id, T1, [row()])
    insert_baseline(db_session, run_id)
    return run_id


# --- sync_indicator --------------------------------------------------------


@pytest.mark.db
def test_sync_indicator_new_is_version_one(db_session: Session) -> None:
    setup_source(db_session)
    assert count(db_session, "indicator") >= 1
    stored = db_session.execute(
        text("select current_version, source_id from indicator where id = 'ind-a'")
    ).one()
    assert tuple(stored) == (1, "obs-src")
    versions = db_session.execute(
        text("select version, length(digest) from indicator_version where indicator_id = 'ind-a'")
    ).all()
    assert [tuple(v) for v in versions] == [(1, 64)]


@pytest.mark.db
def test_sync_indicator_changed_content_is_next_version(db_session: Session) -> None:
    setup_source(db_session)
    assert sync_indicator(db_session, spec(unit="count")) == 2
    current = scalar(db_session, "select current_version from indicator where id = 'ind-a'")
    assert current == 2
    versions = scalar(
        db_session, "select count(*) from indicator_version where indicator_id = 'ind-a'"
    )
    assert versions == 2


@pytest.mark.db
def test_sync_indicator_same_content_writes_nothing(db_session: Session) -> None:
    setup_source(db_session)
    before = (count(db_session, "indicator"), count(db_session, "indicator_version"))
    assert sync_indicator(db_session, spec()) == 1
    assert (count(db_session, "indicator"), count(db_session, "indicator_version")) == before


@pytest.mark.db
@pytest.mark.parametrize("direction", ["up", "down", "none"])
def test_valid_deterioration_directions(db_session: Session, direction: str) -> None:
    setup_source(db_session)
    assert sync_indicator(db_session, spec("ind-d", deterioration_direction=direction)) == 1


@pytest.mark.db
def test_invalid_deterioration_direction_raises_value_error(db_session: Session) -> None:
    setup_source(db_session)
    before = count(db_session, "indicator")
    with pytest.raises(ValueError):
        sync_indicator(db_session, spec("ind-bad", deterioration_direction="sideways"))
    assert count(db_session, "indicator") == before


# --- write_observations ----------------------------------------------------


@pytest.mark.db
def test_new_key_is_written(db_session: Session) -> None:
    run_id = setup_source(db_session)
    result = load(db_session, run_id, T1, [row(), row(geo="FRA")])
    assert (result.written, result.unchanged) == (2, 0)
    assert count(db_session, "observation") == 2


@pytest.mark.db
def test_same_value_on_a_later_release_is_unchanged(db_session: Session) -> None:
    run_id = setup_source(db_session)
    load(db_session, run_id, T1, [row(value_low=0.5, value_high=1.5)])
    result = load(db_session, run_id, T2, [row(value_low=0.5, value_high=1.5)])
    assert (result.written, result.unchanged) == (0, 1)
    assert count(db_session, "observation") == 1


@pytest.mark.db
@pytest.mark.parametrize(
    "change",
    [{"value": 2.0}, {"value_low": 0.25}, {"value_high": 1.75}],
    ids=lambda c: next(iter(c)),
)
def test_each_value_field_changing_writes_a_new_row(
    db_session: Session, change: dict[str, float]
) -> None:
    run_id = setup_source(db_session)
    base = {"value": 1.0, "value_low": 0.5, "value_high": 1.5}
    load(db_session, run_id, T1, [row(**base)])
    result = load(db_session, run_id, T2, [row(**{**base, **change})])
    assert (result.written, result.unchanged) == (1, 0)
    assert count(db_session, "observation") == 2


@pytest.mark.db
def test_null_to_number_in_value_low_is_a_change(db_session: Session) -> None:
    run_id = setup_source(db_session)
    load(db_session, run_id, T1, [row()])
    result = load(db_session, run_id, T2, [row(value_low=0.5)])
    assert (result.written, result.unchanged) == (1, 0)
    latest = observations_as_of(db_session, "ind-a", T2)
    assert [o.value_low for o in latest] == [0.5]


@pytest.mark.db
def test_row_absent_from_a_later_release_keeps_its_last_vintage(db_session: Session) -> None:
    run_id = setup_source(db_session)
    load(db_session, run_id, T1, [row(geo="AAA", value=1.0), row(geo="BBB", value=7.0)])
    result = load(db_session, run_id, T2, [row(geo="AAA", value=2.0)])
    assert (result.written, result.unchanged) == (1, 0)
    latest = {
        o.geo_ref: (o.value, o.retrieved_at) for o in observations_as_of(db_session, "ind-a", T3)
    }
    assert latest == {"AAA": (2.0, T2), "BBB": (7.0, T1)}
    assert count(db_session, "observation") == 3


@pytest.mark.db
def test_duplicate_key_in_one_call_raises_and_writes_nothing(db_session: Session) -> None:
    run_id = setup_source(db_session)
    release_id = release(db_session, "obs-src", run_id, T1)
    rows = [row(geo="OK"), row(value=1.0), row(value=2.0)]
    with pytest.raises(ValueError):
        write_observations(db_session, release_id, run_id, rows)
    assert count(db_session, "observation") == 0


@pytest.mark.db
@pytest.mark.parametrize("bad", [float("nan"), float("inf"), float("-inf")], ids=str)
def test_non_finite_values_raise_and_write_nothing(db_session: Session, bad: float) -> None:
    run_id = setup_source(db_session)
    release_id = release(db_session, "obs-src", run_id, T1)
    for rows in ([row(geo="OK"), row(value=bad)], [row(geo="OK"), row(value_high=bad)]):
        with pytest.raises(ValueError):
            write_observations(db_session, release_id, run_id, rows)
    assert count(db_session, "observation") == 0


@pytest.mark.db
def test_rows_in_two_retrieval_months_land_in_separate_partitions(db_session: Session) -> None:
    run_id = setup_source(db_session)
    load(db_session, run_id, T1, [row(geo="AAA"), row(geo="BBB")])
    load(db_session, run_id, T2, [row(geo="AAA", value=2.0)])
    load(db_session, run_id, T3, [row(geo="AAA", value=3.0)])
    parts = db_session.execute(
        text(
            "select tableoid::regclass::text as part, retrieved_at from observation "
            "order by retrieved_at, geo_ref"
        )
    ).all()
    by_month: dict[int, set[str]] = {}
    for part, retrieved_at in parts:
        by_month.setdefault(retrieved_at.month, set()).add(part)
    assert {m: len(p) for m, p in by_month.items()} == {1: 1, 2: 1, 3: 1}
    assert len({next(iter(p)) for p in by_month.values()}) == 3
    children = db_session.execute(
        text("select count(*) from pg_inherits where inhparent = 'observation'::regclass")
    ).scalar_one()
    assert children >= 3


@pytest.mark.db
def test_retrieved_at_comes_from_the_release(db_session: Session) -> None:
    run_id = setup_source(db_session)
    release_id = release(db_session, "obs-src", run_id, T2)
    write_observations(db_session, release_id, run_id, [row(), row(geo="FRA")])
    stored = db_session.execute(
        text("select distinct retrieved_at, vintage_release_id, run_id from observation")
    ).all()
    assert [tuple(s) for s in stored] == [(T2, release_id, run_id)]


# --- observations_as_of ----------------------------------------------------


@pytest.fixture
def vintages(db_session: Session) -> uuid.UUID:
    """ind-a / USA / January: 1.0 at T1, 2.0 at T2, unchanged at T3. FRA first seen at T2."""
    run_id = setup_source(db_session)
    load(db_session, run_id, T1, [row(value=1.0)])
    load(db_session, run_id, T2, [row(value=2.0), row(geo="FRA", value=5.0)])
    load(db_session, run_id, T3, [row(value=2.0)])
    return run_id


def values(session: Session, as_of: datetime.datetime, **kw: Any) -> list[tuple[str, float]]:
    return [(o.geo_ref, o.value) for o in observations_as_of(session, "ind-a", as_of, **kw)]


@pytest.mark.db
def test_as_of_exact_boundary_includes_that_vintage(db_session: Session, vintages: Any) -> None:
    assert values(db_session, T2) == [("FRA", 5.0), ("USA", 2.0)]
    assert values(db_session, T1) == [("USA", 1.0)]


@pytest.mark.db
def test_as_of_before_the_first_vintage_is_empty(db_session: Session, vintages: Any) -> None:
    assert values(db_session, T1 - datetime.timedelta(seconds=1)) == []


@pytest.mark.db
def test_as_of_between_two_vintages_returns_the_earlier(db_session: Session, vintages: Any) -> None:
    assert values(db_session, T2 - datetime.timedelta(seconds=1)) == [("USA", 1.0)]


@pytest.mark.db
def test_as_of_after_the_last_vintage_returns_the_latest(
    db_session: Session, vintages: Any
) -> None:
    far = T3 + datetime.timedelta(days=365)
    assert values(db_session, far) == [("FRA", 5.0), ("USA", 2.0)]


@pytest.mark.db
def test_key_first_seen_after_as_of_is_absent(db_session: Session, vintages: Any) -> None:
    assert "FRA" not in {geo for geo, _ in values(db_session, T1 + datetime.timedelta(days=1))}


@pytest.mark.db
def test_as_of_geo_ref_filter(db_session: Session, vintages: Any) -> None:
    assert values(db_session, T3, geo_ref="FRA") == [("FRA", 5.0)]
    assert values(db_session, T3, geo_ref="XXX") == []


@pytest.mark.db
def test_as_of_returns_stored_observations_with_provenance(
    db_session: Session, vintages: uuid.UUID
) -> None:
    (obs,) = observations_as_of(db_session, "ind-a", T1)
    assert (obs.indicator_id, obs.geo_ref, obs.period_start, obs.period_end) == (
        "ind-a",
        "USA",
        JAN,
        JAN_END,
    )
    assert (obs.value, obs.value_low, obs.value_high) == (1.0, None, None)
    assert (obs.retrieved_at, obs.run_id) == (T1, vintages)
    release_id = scalar(db_session, "select id from dataset_release where retrieved_at = :t", t=T1)
    assert obs.vintage_release_id == release_id


@pytest.mark.db
def test_as_of_sorts_by_geo_then_start_then_end(db_session: Session) -> None:
    run_id = setup_source(db_session)
    keys = [
        ("BBB", JAN, JAN_END),
        ("AAA", FEB, FEB_END),
        ("AAA", JAN, FEB_END),
        ("AAA", JAN, JAN_END),
        ("BBB", FEB, FEB_END),
    ]
    load(db_session, run_id, T1, [row(geo=g, start=s, end=e) for g, s, e in keys])
    got = [
        (o.geo_ref, o.period_start, o.period_end)
        for o in observations_as_of(db_session, "ind-a", T1)
    ]
    assert got == sorted(keys)


# --- observation_digest ----------------------------------------------------


def digest_rows() -> list[Any]:
    return [row(geo="AAA", value=0.1 + 0.2), row(geo="BBB", value=3.0, value_low=2.0)]


@pytest.fixture
def make_db(database_url: str, monkeypatch: pytest.MonkeyPatch) -> Iterator[Callable[[], Engine]]:
    """Create and migrate databases of their own; the last one made is CANARY_DATABASE_URL."""
    engines: list[Engine] = []

    def make() -> Engine:
        name = f"canary_obs_{uuid.uuid4().hex[:12]}"
        admin = create_engine(database_url, isolation_level="AUTOCOMMIT")
        with admin.connect() as connection:
            connection.execute(text(f'create database "{name}"'))
        admin.dispose()
        url = make_url(database_url).set(database=name).render_as_string(hide_password=False)
        monkeypatch.setenv("CANARY_DATABASE_URL", url)
        command.upgrade(Config("alembic.ini"), "head")
        engines.append(create_engine(url))
        return engines[-1]

    yield make
    for engine in engines:
        engine.dispose()


@pytest.mark.db
def test_digest_is_equal_across_databases_with_different_ids_and_timestamps(
    make_db: Callable[[], Engine],
) -> None:
    digests = []
    for retrieved_at in (T1, T3):
        with Session(make_db()) as session:
            run_id = setup_source(session)
            load(session, run_id, retrieved_at, digest_rows())
            digests.append(observation_digest(session, "obs-src"))
    assert digests[0] == digests[1]
    assert len(digests[0]) == 64


@pytest.mark.db
def test_digest_differs_when_a_value_differs(make_db: Callable[[], Engine]) -> None:
    digests = []
    for second in (3.0, 3.5):
        with Session(make_db()) as session:
            run_id = setup_source(session)
            load(session, run_id, T1, [row(geo="AAA", value=1.0), row(geo="BBB", value=second)])
            digests.append(observation_digest(session, "obs-src"))
    assert digests[0] != digests[1]


@pytest.mark.db
def test_digest_as_of_ignores_later_vintages(db_session: Session, vintages: Any) -> None:
    early = observation_digest(db_session, "obs-src", T1)
    assert early != observation_digest(db_session, "obs-src", T2)
    assert early == observation_digest(db_session, "obs-src", T1 + datetime.timedelta(days=1))
    assert observation_digest(db_session, "obs-src") == observation_digest(
        db_session, "obs-src", T3
    )


# --- write rules -----------------------------------------------------------


@pytest.mark.db
@pytest.mark.parametrize(
    "sql",
    [
        "update observation set value = value + 1",
        "delete from observation",
        "truncate observation",
        "update indicator_version set digest = 'x'",
        "delete from indicator_version",
        "truncate indicator_version",
        "update baseline set method_version = 'x'",
        "delete from baseline",
        "truncate baseline",
        "delete from indicator",
        "truncate indicator cascade",
    ],
)
def test_write_rules_refuse(db_session: Session, loaded: uuid.UUID, sql: str) -> None:
    refused(db_session, sql)


@pytest.mark.db
def test_indicator_still_allows_update(db_session: Session, loaded: uuid.UUID) -> None:
    db_session.execute(text("update indicator set record = '{}' where id = 'ind-a'"))
    assert scalar(db_session, "select record::text from indicator where id = 'ind-a'") == "{}"


@pytest.mark.db
def test_truncate_of_a_single_partition_is_refused(db_session: Session, loaded: uuid.UUID) -> None:
    partition = scalar(db_session, "select tableoid::regclass::text from observation limit 1")
    refused(db_session, f"truncate {partition}")


@pytest.mark.db
def test_partition_rows_refuse_update_and_delete_directly(
    db_session: Session, loaded: uuid.UUID
) -> None:
    partition = scalar(db_session, "select tableoid::regclass::text from observation limit 1")
    refused(db_session, f"update {partition} set value = 9")
    refused(db_session, f"delete from {partition}")


@pytest.mark.db
def test_period_end_before_period_start_is_refused(db_session: Session, loaded: uuid.UUID) -> None:
    with pytest.raises(sqlalchemy.exc.DBAPIError):
        with db_session.begin_nested():
            insert_observation(db_session, loaded, JAN_END, JAN)
    with db_session.begin_nested():
        insert_observation(db_session, loaded, JAN, JAN)


@pytest.mark.db
@pytest.mark.parametrize("horizon", ["12m", "5y", "full"])
def test_baseline_accepts_the_three_horizons(
    db_session: Session, loaded: uuid.UUID, horizon: str
) -> None:
    insert_baseline(db_session, loaded, horizon)


@pytest.mark.db
@pytest.mark.parametrize("horizon", ["3y", "", "FULL"])
def test_baseline_refuses_other_horizons(
    db_session: Session, loaded: uuid.UUID, horizon: str
) -> None:
    with pytest.raises(sqlalchemy.exc.DBAPIError):
        with db_session.begin_nested():
            insert_baseline(db_session, loaded, horizon)


# --- table_counts ----------------------------------------------------------


@pytest.mark.db
def test_table_counts_keys_and_values(db_session: Session) -> None:
    before = table_counts(db_session)
    assert set(before) == set(TABLES)
    run_id = setup_source(db_session)
    load(db_session, run_id, T1, [row(), row(geo="FRA")])
    after = table_counts(db_session)
    for table in TABLES:
        assert after[table] == count(db_session, table)
    assert after["observation"] == before["observation"] + 2
    assert after["indicator"] == before["indicator"] + 1
    assert after["indicator_version"] == before["indicator_version"] + 1
    assert after["dataset_release"] == before["dataset_release"] + 1
    assert after["source"] == before["source"] + 1


# --- CLI -------------------------------------------------------------------


@pytest.mark.db
def test_cli_status_prints_sorted_counts(
    make_db: Callable[[], Engine], capsys: pytest.CaptureFixture[str]
) -> None:
    engine = make_db()
    with Session(engine) as session:
        run_id = setup_source(session)
        load(session, run_id, T1, [row(), row(geo="FRA")])
        session.commit()
    with engine.connect() as connection:
        expected = [
            f"{t} {connection.execute(text(f'select count(*) from {t}')).scalar_one()}"
            for t in TABLES
        ]
    capsys.readouterr()
    assert main(["status"]) == 0
    lines = capsys.readouterr().out.splitlines()
    assert lines == expected
    assert "observation 2" in lines
    assert lines == sorted(lines)


def test_cli_status_without_database_url_returns_2(
    monkeypatch: pytest.MonkeyPatch, capsys: pytest.CaptureFixture[str]
) -> None:
    monkeypatch.delenv("CANARY_DATABASE_URL", raising=False)
    assert main(["status"]) == 2
    assert "CANARY_DATABASE_URL" in capsys.readouterr().err
