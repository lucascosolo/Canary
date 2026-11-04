"""Provenance spine: write rules, registry sync, releases, health report and CLI."""

from __future__ import annotations

import datetime
import pathlib
import uuid
from collections.abc import Iterator
from typing import Any

import pytest
import sqlalchemy.exc
import yaml
from alembic import command
from alembic.config import Config
from sqlalchemy import Engine, create_engine, text
from sqlalchemy.engine import make_url
from sqlalchemy.orm import Session

from canary.cli import main
from canary.provenance import (
    finish_run,
    health_report,
    record_health,
    record_release,
    start_run,
    sync_registry,
)
from canary.registry import SourceEntry

UTC = datetime.UTC
NOW = datetime.datetime(2026, 11, 4, 12, 0, tzinfo=UTC)
STAGES = [
    "ingest",
    "normalise",
    "extract",
    "support_check",
    "lineage",
    "event_assembly",
    "indicator",
    "baseline",
    "change_detection",
    "watch_rules",
    "coverage",
    "embed",
    "translate",
    "draft",
]


def entry_data(source_id: str, **overrides: Any) -> dict[str, Any]:
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
    data.update(overrides)
    return data


def make_entry(source_id: str, **overrides: Any) -> SourceEntry:
    return SourceEntry.model_validate(
        entry_data(source_id, **overrides), context={"today": datetime.date(2026, 11, 4)}
    )


def new_run(session: Session, stage: str = "ingest") -> uuid.UUID:
    return start_run(session, stage, code_commit="abc123", config_digest="cfg")


def count(session: Session, table: str) -> int:
    return session.execute(text(f"select count(*) from {table}")).scalar_one()


def release(
    session: Session, source_id: str, run_id: uuid.UUID, digest: str = "d1", **kw: Any
) -> tuple[uuid.UUID, bool]:
    args: dict[str, Any] = {
        "version_label": "v1",
        "content_digest": digest,
        "row_count": 10,
        "schema_digest": "s1",
        "licence_snapshot": "CC-BY-4.0",
        "file_refs": {"files": []},
        "run_id": run_id,
    }
    args.update(kw)
    return record_release(session, source_id, **args)


def refused(session: Session, sql: str, **params: Any) -> None:
    with pytest.raises(sqlalchemy.exc.DBAPIError):
        with session.begin_nested():
            session.execute(text(sql), params)


@pytest.fixture
def seeded(db_session: Session) -> uuid.UUID:
    """One source with a version, a health check and a release; returns the open run id."""
    run_id = new_run(db_session)
    sync_registry(db_session, [make_entry("seed-src")], run_id=run_id)
    record_health(db_session, "seed-src", ok=True)
    release(db_session, "seed-src", run_id)
    return run_id


# --- pipeline_run ----------------------------------------------------------


@pytest.mark.db
@pytest.mark.parametrize("stage", STAGES)
def test_every_stage_is_accepted(db_session: Session, stage: str) -> None:
    run_id = new_run(db_session, stage)
    stored = db_session.execute(
        text(
            "select stage, ended_at, input_count, output_count, error_count "
            "from pipeline_run where id = :i"
        ),
        {"i": run_id},
    ).one()
    assert tuple(stored) == (stage, None, 0, 0, 0)


@pytest.mark.db
def test_unknown_stage_is_refused(db_session: Session) -> None:
    with pytest.raises(sqlalchemy.exc.DBAPIError):
        with db_session.begin_nested():
            new_run(db_session, "bogus")


@pytest.mark.db
def test_start_run_rejects_unknown_keyword(db_session: Session) -> None:
    with pytest.raises(TypeError):
        start_run(db_session, "ingest", code_commit="a", config_digest="b", colour="red")  # type: ignore[call-arg]


@pytest.mark.db
def test_start_run_accepts_version_fields_and_notes(db_session: Session) -> None:
    run_id = start_run(
        db_session,
        "extract",
        code_commit="a",
        config_digest="b",
        model_id="m",
        prompt_version="p",
        schema_version="s",
        indicator_catalog_version="i",
        rule_file_version="r",
        notes="n",
    )
    row = db_session.execute(
        text(
            "select model_id, prompt_version, schema_version, indicator_catalog_version, "
            "rule_file_version, notes from pipeline_run where id = :i"
        ),
        {"i": run_id},
    ).one()
    assert tuple(row) == ("m", "p", "s", "i", "r", "n")


@pytest.mark.db
def test_finish_run_closes_the_run(db_session: Session) -> None:
    run_id = new_run(db_session)
    finish_run(db_session, run_id, input_count=5, output_count=4, error_count=1, notes="done")
    row = db_session.execute(
        text(
            "select ended_at, input_count, output_count, error_count, notes, stage "
            "from pipeline_run where id = :i"
        ),
        {"i": run_id},
    ).one()
    assert row.ended_at is not None
    assert (row.input_count, row.output_count, row.error_count, row.notes) == (5, 4, 1, "done")
    assert row.stage == "ingest"


@pytest.mark.db
def test_second_update_after_closing_is_refused(db_session: Session) -> None:
    run_id = new_run(db_session)
    finish_run(db_session, run_id)
    with pytest.raises(sqlalchemy.exc.DBAPIError):
        with db_session.begin_nested():
            finish_run(db_session, run_id, output_count=9)
    refused(db_session, "update pipeline_run set notes = 'x' where id = :i", i=run_id)


@pytest.mark.db
@pytest.mark.parametrize(
    "assignment",
    [
        "stage = 'lineage'",
        "stage = 'lineage', ended_at = now()",
        "code_commit = 'other', ended_at = now()",
        "started_at = now(), ended_at = now()",
        "notes = 'only notes'",
    ],
)
def test_other_updates_on_an_open_run_are_refused(db_session: Session, assignment: str) -> None:
    run_id = new_run(db_session)
    refused(db_session, f"update pipeline_run set {assignment} where id = :i", i=run_id)


@pytest.mark.db
def test_pipeline_run_delete_is_refused(db_session: Session) -> None:
    run_id = new_run(db_session)
    refused(db_session, "delete from pipeline_run where id = :i", i=run_id)


# --- the other tables ------------------------------------------------------

UPDATES = {
    "source_version": "update source_version set digest = 'x'",
    "source_health": "update source_health set ok = not ok",
    "dataset_release": "update dataset_release set row_count = row_count + 1",
}


@pytest.mark.db
@pytest.mark.parametrize("table", list(UPDATES))
def test_append_only_tables_refuse_update(
    db_session: Session, seeded: uuid.UUID, table: str
) -> None:
    refused(db_session, UPDATES[table])


@pytest.mark.db
@pytest.mark.parametrize("table", [*UPDATES, "source", "pipeline_run"])
def test_no_table_allows_delete(db_session: Session, seeded: uuid.UUID, table: str) -> None:
    refused(db_session, f"delete from {table}")


@pytest.mark.db
@pytest.mark.parametrize(
    "table", ["pipeline_run", "source", "source_version", "source_health", "dataset_release"]
)
def test_truncate_is_refused(db_session: Session, seeded: uuid.UUID, table: str) -> None:
    refused(db_session, f"truncate {table} cascade")


@pytest.mark.db
def test_source_allows_update(db_session: Session, seeded: uuid.UUID) -> None:
    db_session.execute(text("update source set status = 'degraded' where id = 'seed-src'"))
    status = db_session.execute(text("select status from source where id = 'seed-src'"))
    assert status.scalar_one() == "degraded"


# --- sync_registry ---------------------------------------------------------


@pytest.mark.db
def test_sync_adds_new_sources_with_version_one(db_session: Session) -> None:
    run_id = new_run(db_session)
    entries = [make_entry("c-src"), make_entry("a-src"), make_entry("b-src")]
    result = sync_registry(db_session, entries, run_id=run_id)
    assert result.added == ["a-src", "b-src", "c-src"]
    assert result.changed == result.unchanged == result.missing == []
    rows = db_session.execute(
        text("select id, current_version, canary_use, status from source order by id")
    ).all()
    assert [tuple(r) for r in rows] == [(s, 1, "open", "lead") for s in ("a-src", "b-src", "c-src")]
    versions = db_session.execute(
        text("select source_id, version, run_id, length(digest) from source_version order by 1")
    ).all()
    assert [tuple(v) for v in versions] == [(s, 1, run_id, 64) for s in ("a-src", "b-src", "c-src")]


@pytest.mark.db
def test_sync_changed_entry_gets_next_version(db_session: Session) -> None:
    first = new_run(db_session)
    sync_registry(db_session, [make_entry("a-src"), make_entry("b-src")], run_id=first)
    second = new_run(db_session)
    result = sync_registry(
        db_session, [make_entry("a-src", status="degraded"), make_entry("b-src")], run_id=second
    )
    assert (result.added, result.changed, result.unchanged, result.missing) == (
        [],
        ["a-src"],
        ["b-src"],
        [],
    )
    source = db_session.execute(
        text("select current_version, status from source where id = 'a-src'")
    ).one()
    assert tuple(source) == (2, "degraded")
    versions = db_session.execute(
        text("select version, run_id from source_version where source_id = 'a-src' order by 1")
    ).all()
    assert [tuple(v) for v in versions] == [(1, first), (2, second)]
    distinct = db_session.execute(
        text("select count(distinct digest) from source_version where source_id = 'a-src'")
    ).scalar_one()
    assert distinct == 2
    assert count(db_session, "source_version") == 3


@pytest.mark.db
def test_second_identical_sync_writes_no_rows(db_session: Session) -> None:
    entries = [make_entry("a-src"), make_entry("b-src")]
    sync_registry(db_session, entries, run_id=new_run(db_session))
    before = (count(db_session, "source"), count(db_session, "source_version"))
    result = sync_registry(db_session, entries, run_id=new_run(db_session))
    assert (result.added, result.changed, result.unchanged) == ([], [], ["a-src", "b-src"])
    assert (count(db_session, "source"), count(db_session, "source_version")) == before


@pytest.mark.db
def test_missing_source_is_reported_and_left_in_place(db_session: Session) -> None:
    both = [make_entry("a-src"), make_entry("b-src")]
    sync_registry(db_session, both, run_id=new_run(db_session))
    before = count(db_session, "source_version")
    result = sync_registry(db_session, [make_entry("a-src")], run_id=new_run(db_session))
    assert result.missing == ["b-src"]
    assert result.unchanged == ["a-src"]
    version = db_session.execute(text("select current_version from source where id = 'b-src'"))
    assert version.scalar_one() == 1
    assert count(db_session, "source_version") == before


# --- record_release --------------------------------------------------------


@pytest.mark.db
def test_record_release_is_idempotent_on_content_digest(db_session: Session) -> None:
    first_run = new_run(db_session)
    sync_registry(db_session, [make_entry("a-src")], run_id=first_run)
    first_id, written = release(db_session, "a-src", first_run, version_label="2026-10")
    assert written is True
    assert isinstance(first_id, uuid.UUID)
    again_id, written_again = release(
        db_session, "a-src", new_run(db_session), version_label="2026-11"
    )
    assert (again_id, written_again) == (first_id, False)
    assert count(db_session, "dataset_release") == 1
    other_id, written_other = release(db_session, "a-src", first_run, digest="d2")
    assert written_other is True
    assert other_id != first_id
    assert count(db_session, "dataset_release") == 2


# --- health_report ---------------------------------------------------------


def report_for(session: Session, source_id: str) -> Any:
    return {r.source_id: r for r in health_report(session, now=NOW)}[source_id]


def sync_one(session: Session, source_id: str = "h-src", **overrides: Any) -> uuid.UUID:
    run_id = new_run(session)
    sync_registry(session, [make_entry(source_id, **overrides)], run_id=run_id)
    return run_id


def ago(**kwargs: float) -> datetime.datetime:
    return NOW - datetime.timedelta(**kwargs)


@pytest.mark.db
def test_never_fetched_without_any_ok_check(db_session: Session) -> None:
    sync_one(db_session, expected_lag_days=2)
    row = report_for(db_session, "h-src")
    assert (row.freshness, row.last_ok_at, row.last_failure_at) == ("never_fetched", None, None)
    assert (row.status, row.canary_use, row.expected_lag_days) == ("lead", "open", 2)


@pytest.mark.db
def test_failed_checks_do_not_count_as_ok(db_session: Session) -> None:
    sync_one(db_session, expected_lag_days=2)
    record_health(db_session, "h-src", ok=False, checked_at=ago(hours=1))
    row = report_for(db_session, "h-src")
    assert row.freshness == "never_fetched"
    assert row.last_ok_at is None
    assert row.last_failure_at == ago(hours=1)


@pytest.mark.db
def test_last_ok_and_last_failure_are_the_latest_of_each(db_session: Session) -> None:
    sync_one(db_session, expected_lag_days=2)
    record_health(db_session, "h-src", ok=True, checked_at=ago(days=3))
    record_health(db_session, "h-src", ok=True, checked_at=ago(days=1))
    record_health(db_session, "h-src", ok=False, checked_at=ago(days=2))
    record_health(db_session, "h-src", ok=False, checked_at=ago(hours=2))
    row = report_for(db_session, "h-src")
    assert (row.last_ok_at, row.last_failure_at, row.freshness) == (
        ago(days=1),
        ago(hours=2),
        "fresh",
    )


@pytest.mark.db
def test_unknown_when_ok_but_no_expected_lag(db_session: Session) -> None:
    sync_one(db_session)
    record_health(db_session, "h-src", ok=True, checked_at=ago(days=400))
    row = report_for(db_session, "h-src")
    assert (row.freshness, row.expected_lag_days) == ("unknown", None)


@pytest.mark.db
def test_boundary_exactly_expected_lag_is_fresh(db_session: Session) -> None:
    sync_one(db_session, expected_lag_days=2)
    record_health(db_session, "h-src", ok=True, checked_at=ago(days=2))
    assert report_for(db_session, "h-src").freshness == "fresh"


@pytest.mark.db
def test_beyond_expected_lag_is_stale(db_session: Session) -> None:
    sync_one(db_session, expected_lag_days=2)
    record_health(db_session, "h-src", ok=True, checked_at=ago(days=2, seconds=1))
    assert report_for(db_session, "h-src").freshness == "stale"


@pytest.mark.db
def test_zero_lag_boundary(db_session: Session) -> None:
    sync_one(db_session, expected_lag_days=0)
    record_health(db_session, "h-src", ok=True, checked_at=NOW)
    assert report_for(db_session, "h-src").freshness == "fresh"


@pytest.mark.db
def test_last_ok_comes_from_a_later_release(db_session: Session) -> None:
    run_id = sync_one(db_session, expected_lag_days=2)
    record_health(db_session, "h-src", ok=True, checked_at=ago(days=10))
    release(db_session, "h-src", run_id, retrieved_at=ago(hours=3))
    row = report_for(db_session, "h-src")
    assert (row.last_ok_at, row.freshness) == (ago(hours=3), "fresh")


@pytest.mark.db
def test_release_alone_makes_a_source_fetched(db_session: Session) -> None:
    run_id = sync_one(db_session, expected_lag_days=2)
    release(db_session, "h-src", run_id, retrieved_at=ago(days=5))
    assert report_for(db_session, "h-src").freshness == "stale"


@pytest.mark.db
def test_report_is_sorted_by_id_and_covers_every_source(db_session: Session) -> None:
    entries = [make_entry("m-src"), make_entry("z-src"), make_entry("a-src")]
    sync_registry(db_session, entries, run_id=new_run(db_session))
    ids = [r.source_id for r in health_report(db_session, now=NOW)]
    assert ids == sorted(ids)
    assert {"a-src", "m-src", "z-src"} <= set(ids)


# --- CLI -------------------------------------------------------------------


@pytest.fixture
def cli_engine(database_url: str, monkeypatch: pytest.MonkeyPatch) -> Iterator[Engine]:
    """A fresh, migrated database of its own, because CLI commands commit for real."""
    name = f"canary_cli_{uuid.uuid4().hex[:12]}"
    admin = create_engine(database_url, isolation_level="AUTOCOMMIT")
    with admin.connect() as connection:
        connection.execute(text(f'create database "{name}"'))
    admin.dispose()
    url = make_url(database_url).set(database=name).render_as_string(hide_password=False)
    monkeypatch.setenv("CANARY_DATABASE_URL", url)
    command.upgrade(Config("alembic.ini"), "head")
    engine = create_engine(url)
    yield engine
    engine.dispose()


def registry_dir(tmp_path: pathlib.Path, *ids: str) -> pathlib.Path:
    directory = tmp_path / "registry"
    directory.mkdir()
    for source_id in ids:
        (directory / f"{source_id}.yaml").write_text(
            yaml.safe_dump(entry_data(source_id)), encoding="utf-8"
        )
    return directory


def cli_count(engine: Engine, table: str) -> int:
    with engine.connect() as connection:
        return connection.execute(text(f"select count(*) from {table}")).scalar_one()


@pytest.mark.db
def test_cli_sync_reports_and_a_second_run_reports_unchanged(
    cli_engine: Engine, tmp_path: pathlib.Path, capsys: pytest.CaptureFixture[str]
) -> None:
    path = str(registry_dir(tmp_path, "a-src", "b-src"))
    assert main(["registry", "sync", "--path", path]) == 0
    assert "added 2, changed 0, unchanged 0, missing 0" in capsys.readouterr().out
    assert cli_count(cli_engine, "source") == 2
    assert main(["registry", "sync", "--path", path]) == 0
    assert "added 0, changed 0, unchanged 2, missing 0" in capsys.readouterr().out
    assert cli_count(cli_engine, "source_version") == 2
    with cli_engine.connect() as connection:
        runs = connection.execute(
            text("select stage, ended_at is not null from pipeline_run")
        ).all()
    assert [tuple(r) for r in runs] == [("ingest", True), ("ingest", True)]


@pytest.mark.db
def test_cli_sync_invalid_registry_returns_1_and_writes_nothing(
    cli_engine: Engine, tmp_path: pathlib.Path, capsys: pytest.CaptureFixture[str]
) -> None:
    path = registry_dir(tmp_path)
    bad = entry_data("bad-one", status="dreaming")
    (path / "bad-one.yaml").write_text(yaml.safe_dump(bad), encoding="utf-8")
    assert main(["registry", "sync", "--path", str(path)]) == 1
    assert "bad-one.yaml" in capsys.readouterr().err
    for table in ("source", "source_version", "pipeline_run"):
        assert cli_count(cli_engine, table) == 0


@pytest.mark.db
def test_cli_health_line_format(
    cli_engine: Engine, tmp_path: pathlib.Path, capsys: pytest.CaptureFixture[str]
) -> None:
    path = str(registry_dir(tmp_path, "a-src", "b-src"))
    assert main(["registry", "sync", "--path", path]) == 0
    with Session(cli_engine) as session:
        record_health(session, "a-src", ok=True)
        session.commit()
    capsys.readouterr()
    assert main(["health"]) == 0
    lines = capsys.readouterr().out.splitlines()
    assert len(lines) == 2
    first = lines[0].split(" ")
    assert first[:2] == ["a-src", "unknown"]
    assert len(first) == 3 and first[2] != "never"
    assert lines[1] == "b-src never_fetched never"


@pytest.mark.parametrize("argv", [["registry", "sync"], ["health"]])
def test_cli_without_database_url_returns_2(
    argv: list[str],
    tmp_path: pathlib.Path,
    monkeypatch: pytest.MonkeyPatch,
    capsys: pytest.CaptureFixture[str],
) -> None:
    monkeypatch.delenv("CANARY_DATABASE_URL", raising=False)
    if argv[0] == "registry":
        argv = [*argv, "--path", str(registry_dir(tmp_path, "a-src"))]
    assert main(argv) == 2
    assert "CANARY_DATABASE_URL" in capsys.readouterr().err
