"""Ingestion runner, country resolver, place table and the `canary ingest` command."""

from __future__ import annotations

import datetime
import hashlib
import pathlib
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

import canary.geo
from canary.adapters import ADAPTERS
from canary.cli import main
from canary.geo import CountryResolver, load_resolver
from canary.http import Fetcher
from canary.ingest import ingest
from canary.observations import observation_digest, observations_as_of
from canary.provenance import record_health
from canary.rawstore import RawStore
from fixtures.ingest_support import (
    FakeFetcher,
    add_place,
    candidate_routes,
    error_class,
    ert_routes,
    ert_variant_routes,
    fixture,
    ged_routes,
    geonames_routes,
    register,
    scalar,
    seed_places,
    wikidata_routes,
)


@pytest.fixture
def store(tmp_path: pathlib.Path) -> RawStore:
    return RawStore(tmp_path / "raw")


@pytest.fixture
def make_db(
    database_url: str, monkeypatch: pytest.MonkeyPatch, tmp_path: pathlib.Path
) -> Iterator[Callable[[], Engine]]:
    """Create and migrate databases of their own; the last one made is CANARY_DATABASE_URL."""
    monkeypatch.setenv("CANARY_RAW_DIR", str(tmp_path / "rawdir"))
    monkeypatch.setenv("CANARY_DROP_DIR", str(tmp_path / "dropdir"))
    engines: list[Engine] = []

    def make() -> Engine:
        name = f"canary_ing_{uuid.uuid4().hex[:12]}"
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


def ingest_ert(session: Session, store: RawStore, changed: bool = False) -> Any:
    return ingest(session, ADAPTERS["vdem-ert"](), FakeFetcher(ert_routes(changed)), store)


def failure_state(session: Session, source_id: str) -> None:
    health = session.execute(
        text("select ok, message from source_health where source_id = :s"), {"s": source_id}
    ).all()
    assert [h.ok for h in health] == [False]
    assert health[0].message
    runs = session.execute(
        text("select ended_at, error_count from pipeline_run where error_count > 0")
    ).all()
    assert len(runs) == 1 and runs[0].error_count == 1 and runs[0].ended_at is not None
    assert (
        scalar(session, "select count(*) from dataset_release where source_id = :s", s=source_id)
        == 0
    )
    assert scalar(session, "select count(*) from observation") == 0


# --- NotPermitted ----------------------------------------------------------


@pytest.mark.db
@pytest.mark.parametrize("use", ["links", "unverified", "permission", "excluded"])
def test_source_not_open_or_display_is_refused_before_any_fetch(
    db_session: Session, store: RawStore, use: str
) -> None:
    register(db_session, "vdem-ert", use)
    fetcher = FakeFetcher(ert_routes())
    with pytest.raises(error_class("NotPermitted")):
        ingest(db_session, ADAPTERS["vdem-ert"](), fetcher, store)
    assert fetcher.calls == []


@pytest.mark.db
def test_unregistered_source_is_refused_before_any_fetch(
    db_session: Session, store: RawStore
) -> None:
    fetcher = FakeFetcher(ert_routes())
    with pytest.raises(error_class("NotPermitted")):
        ingest(db_session, ADAPTERS["vdem-ert"](), fetcher, store)
    assert fetcher.calls == []


@pytest.mark.db
def test_display_use_is_permitted(db_session: Session, store: RawStore) -> None:
    seed_places(db_session)
    register(db_session, "vdem-ert", "display")
    assert ingest_ert(db_session, store).new_release is True


# --- Success paths ---------------------------------------------------------


@pytest.mark.db
def test_new_release_writes_observations_and_records_ok_health(
    db_session: Session, store: RawStore
) -> None:
    seed_places(db_session)
    register(db_session, "vdem-ert")
    result = ingest_ert(db_session, store)
    assert (result.source_id, result.version_label, result.new_release) == (
        "vdem-ert",
        "15.0.1",
        True,
    )
    assert (result.written, result.unchanged, result.skipped, result.unmapped) == (7, 0, 0, 0)
    assert scalar(db_session, "select count(*) from observation") == 7
    release = db_session.execute(
        text("select version_label, row_count, licence_snapshot from dataset_release")
    ).one()
    assert release.version_label == "15.0.1" and release.row_count == 7
    assert release.licence_snapshot
    health = db_session.execute(text("select ok, items_seen from source_health")).all()
    assert [(h.ok, h.items_seen) for h in health] == [(True, 7)]
    run = db_session.execute(
        text("select ended_at, error_count, output_count from pipeline_run where output_count = 7")
    ).one()
    assert run.ended_at is not None and run.error_count == 0


@pytest.mark.db
def test_existing_release_writes_nothing_but_records_ok_health(
    db_session: Session, store: RawStore
) -> None:
    seed_places(db_session)
    register(db_session, "vdem-ert")
    ingest_ert(db_session, store)
    again = ingest_ert(db_session, store)
    assert again.new_release is False and again.written == 0
    assert scalar(db_session, "select count(*) from observation") == 7
    assert scalar(db_session, "select count(*) from dataset_release") == 1
    assert scalar(db_session, "select count(*) from source_health where ok") == 2
    assert (
        scalar(
            db_session,
            "select count(*) from pipeline_run "
            "where stage = 'ingest' and ended_at is null and code_commit <> 'seed'",
        )
        == 0
    )


@pytest.mark.db
def test_content_digest_is_sha256_of_sorted_filename_sha_lines(
    db_session: Session, store: RawStore
) -> None:
    seed_places(db_session)
    register(db_session, "vdem-ert")
    ingest_ert(db_session, store)
    stored = scalar(db_session, "select content_digest from dataset_release")
    sha = hashlib.sha256(fixture("vdem-ert", "ert.csv")).hexdigest()
    assert stored == hashlib.sha256(f"ert.csv:{sha}".encode()).hexdigest()


@pytest.mark.db
def test_ucdp_unmapped_names_are_reported_in_the_result(
    db_session: Session, store: RawStore
) -> None:
    seed_places(db_session)
    register(db_session, "ucdp-candidate")
    result = ingest(
        db_session, ADAPTERS["ucdp-candidate"](), FakeFetcher(candidate_routes()), store
    )
    assert (result.written, result.skipped, result.unmapped) == (6, 1, 1)


@pytest.mark.db
def test_a_known_release_is_parsed_again_so_a_newly_mapped_country_is_loaded(
    db_session: Session, store: RawStore
) -> None:
    seed_places(db_session)
    register(db_session, "ucdp-candidate")
    first = ingest(db_session, ADAPTERS["ucdp-candidate"](), FakeFetcher(candidate_routes()), store)
    assert (first.new_release, first.skipped, first.unmapped) == (True, 1, 1)
    name = scalar(
        db_session,
        "select notes from pipeline_run where notes like 'unmapped: %' limit 1",
    ).removeprefix("unmapped: ")
    run_id = scalar(db_session, "select run_id from dataset_release limit 1")
    db_session.execute(
        text(
            "insert into place (id, iso2, name, continent, geonames_id, run_id, current_version) "
            "values ('ZZZ', 'ZZ', :name, 'AF', 1, :run, 1)"
        ),
        {"name": name, "run": run_id},
    )
    again = ingest(db_session, ADAPTERS["ucdp-candidate"](), FakeFetcher(candidate_routes()), store)
    assert (again.new_release, again.skipped, again.unmapped) == (False, 0, 0)
    assert again.written > 0
    assert again.unchanged == first.written
    assert scalar(db_session, "select count(*) from dataset_release") == 1
    third = ingest(db_session, ADAPTERS["ucdp-candidate"](), FakeFetcher(candidate_routes()), store)
    assert (third.new_release, third.written) == (False, 0)


# --- Failure paths ---------------------------------------------------------


@pytest.mark.db
def test_access_refused_leaves_a_failed_health_row_and_reraises(
    db_session: Session, store: RawStore
) -> None:
    seed_places(db_session)
    register(db_session, "vdem-ert")
    refused = error_class("AccessRefused")("https://example.org/x", 403)
    fetcher = FakeFetcher([("", refused)])
    with pytest.raises(error_class("AccessRefused")):
        ingest(db_session, ADAPTERS["vdem-ert"](), fetcher, store)
    failure_state(db_session, "vdem-ert")


@pytest.mark.db
def test_fetch_failed_leaves_a_failed_health_row_and_reraises(
    db_session: Session, store: RawStore
) -> None:
    seed_places(db_session)
    register(db_session, "vdem-ert")
    fetcher = FakeFetcher([("", error_class("FetchFailed")("connection reset"))])
    with pytest.raises(error_class("FetchFailed")):
        ingest(db_session, ADAPTERS["vdem-ert"](), fetcher, store)
    failure_state(db_session, "vdem-ert")


@pytest.mark.db
def test_manual_file_missing_leaves_a_failed_health_row_and_reraises(
    db_session: Session, store: RawStore, tmp_path: pathlib.Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    monkeypatch.setenv("CANARY_DROP_DIR", str(tmp_path / "empty-drop"))
    seed_places(db_session)
    register(db_session, "cline-coups")
    with pytest.raises(error_class("ManualFileMissing")):
        ingest(db_session, ADAPTERS["cline-coups"](), FakeFetcher([]), store)
    failure_state(db_session, "cline-coups")


@pytest.mark.db
def test_schema_changed_leaves_a_failed_health_row_and_reraises(
    db_session: Session, store: RawStore
) -> None:
    seed_places(db_session)
    register(db_session, "vdem-ert")
    with pytest.raises(error_class("SchemaChanged")):
        ingest_ert(db_session, store, changed=True)
    failure_state(db_session, "vdem-ert")


@pytest.mark.db
def test_our_world_in_data_with_an_empty_allow_list_records_no_release(
    db_session: Session, store: RawStore
) -> None:
    register(db_session, "our-world-in-data")
    fetcher = FakeFetcher([])
    ingest(db_session, ADAPTERS["our-world-in-data"](), fetcher, store)
    assert fetcher.calls == []
    assert scalar(db_session, "select count(*) from dataset_release") == 0
    assert scalar(db_session, "select count(*) from observation") == 0


# --- CountryResolver -------------------------------------------------------

RESOLVER = CountryResolver(
    {"Ghana": "GHA", "Côte d'Ivoire": "CIV"}, {"Ivory Coast": "CIV", "Burma": "MMR"}
)


@pytest.mark.parametrize(
    ("name", "expected"),
    [
        ("Ghana", "GHA"),
        ("ghana", "GHA"),
        ("GHANA", "GHA"),
        ("  Ghana \t", "GHA"),
        ("Côte d'Ivoire", "CIV"),
        ("ivory coast", "CIV"),
        (" BURMA ", "MMR"),
    ],
)
def test_resolver_matches_exactly_after_case_folding_and_trimming(name: str, expected: str) -> None:
    assert RESOLVER.resolve(name) == expected


@pytest.mark.parametrize(
    "name", ["Ghan", "Gana", "Republic of Ghana", "Ghana Republic", "", "Burm"]
)
def test_resolver_never_guesses(name: str) -> None:
    assert RESOLVER.resolve(name) is None


@pytest.mark.db
def test_load_resolver_on_an_empty_place_table_says_to_ingest_geonames(db_session: Session) -> None:
    with pytest.raises(error_class("SchemaChanged"), match="geonames"):
        load_resolver(db_session)


@pytest.mark.db
def test_load_resolver_reads_place_names_and_the_alias_file(db_session: Session) -> None:
    seed_places(db_session)
    resolver = load_resolver(db_session)
    assert resolver.resolve("ghana") == "GHA"
    assert resolver.resolve("Atlantis") is None


# --- place table -----------------------------------------------------------


def refused(session: Session, sql: str) -> None:
    with pytest.raises(sqlalchemy.exc.DBAPIError):
        with session.begin_nested():
            session.execute(text(sql))


@pytest.mark.db
def test_place_refuses_delete_and_truncate(db_session: Session) -> None:
    seed_places(db_session)
    refused(db_session, "delete from place where id = 'GHA'")
    refused(db_session, "truncate place")
    assert scalar(db_session, "select count(*) from place") == 3


@pytest.mark.db
def test_place_allows_upserts(db_session: Session) -> None:
    seed_places(db_session)
    db_session.execute(text("update place set name = 'Republic of Ghana' where id = 'GHA'"))
    assert scalar(db_session, "select name from place where id = 'GHA'") == "Republic of Ghana"


# --- GeoNames and Wikidata through the runner ------------------------------


@pytest.mark.db
def test_geonames_ingest_upserts_places(db_session: Session, store: RawStore) -> None:
    register(db_session, "geonames")
    result = ingest(db_session, ADAPTERS["geonames"](), FakeFetcher(geonames_routes()), store)
    assert result.new_release is True and result.written == 0
    rows = db_session.execute(
        text("select id, iso2, name, continent, geonames_id, wikidata_id from place order by id")
    ).all()
    assert [tuple(r) for r in rows] == [
        ("GHA", "GH", "Ghana", "AF", 2300660, None),
        ("MLI", "ML", "Mali", "AF", 2453866, None),
        ("NER", "NE", "Niger", "AF", 2440476, None),
    ]
    assert (
        scalar(db_session, "select version_label from dataset_release")
        == hashlib.sha256(fixture("geonames", "countryInfo.txt")).hexdigest()[:12]
    )


@pytest.mark.db
def test_geonames_changed_header_fails_and_adds_no_places(
    db_session: Session, store: RawStore
) -> None:
    register(db_session, "geonames")
    with pytest.raises(error_class("SchemaChanged")):
        ingest(db_session, ADAPTERS["geonames"](), FakeFetcher(geonames_routes(True)), store)
    assert scalar(db_session, "select count(*) from place") == 0


@pytest.mark.db
def test_wikidata_sets_the_smallest_q_id_on_existing_places_and_adds_none(
    db_session: Session, store: RawStore
) -> None:
    seed_places(db_session)
    register(db_session, "wikidata")
    ingest(db_session, ADAPTERS["wikidata"](), FakeFetcher(wikidata_routes()), store)
    ids = dict(db_session.execute(text("select id, wikidata_id from place")).all())
    assert ids == {"GHA": "Q117", "MLI": "Q912", "NER": None}


# --- Reproducibility -------------------------------------------------------


@pytest.mark.db
def test_two_databases_ingesting_the_same_fixtures_have_equal_digests(
    make_db: Callable[[], Engine], tmp_path: pathlib.Path
) -> None:
    digests = []
    for n in range(2):
        engine = make_db()
        with Session(engine) as session:
            seed_places(session)
            register(session, "vdem-ert")
            register(session, "ucdp-ged")
            ingest(
                session,
                ADAPTERS["vdem-ert"](),
                FakeFetcher(ert_routes()),
                RawStore(tmp_path / f"r{n}"),
            )
            ingest(
                session,
                ADAPTERS["ucdp-ged"](),
                FakeFetcher(ged_routes()),
                RawStore(tmp_path / f"r{n}"),
            )
            session.commit()
        with Session(engine) as session:
            digests.append(
                (observation_digest(session, "vdem-ert"), observation_digest(session, "ucdp-ged"))
            )
    assert digests[0] == digests[1]
    assert digests[0][0] != digests[0][1]


# --- CLI -------------------------------------------------------------------


@pytest.fixture
def cli_db(make_db: Callable[[], Engine]) -> Engine:
    engine = make_db()
    with Session(engine) as session:
        seed_places(session)
        register(session, "vdem-ert")
        register(session, "geonames", "links")
        session.commit()
    return engine


def fake_get(monkeypatch: pytest.MonkeyPatch, routes: list[Any]) -> FakeFetcher:
    fetcher = FakeFetcher(routes)
    monkeypatch.setattr(Fetcher, "get", lambda self, url, **kw: fetcher.get(url, **kw))
    return fetcher


@pytest.mark.db
def test_cli_ingest_prints_the_summary_line_and_returns_0(
    cli_db: Engine, monkeypatch: pytest.MonkeyPatch, capsys: pytest.CaptureFixture[str]
) -> None:
    fake_get(monkeypatch, ert_routes())
    assert main(["ingest", "vdem-ert"]) == 0
    assert capsys.readouterr().out.splitlines() == [
        "vdem-ert 15.0.1 new written=7 unchanged=0 skipped=0 unmapped=0"
    ]
    assert main(["ingest", "vdem-ert"]) == 0
    assert capsys.readouterr().out.splitlines() == [
        "vdem-ert 15.0.1 existing written=0 unchanged=7 skipped=0 unmapped=0"
    ]


@pytest.mark.db
def test_cli_ingest_failure_returns_1_prints_to_stderr_and_keeps_the_failure_record(
    cli_db: Engine, monkeypatch: pytest.MonkeyPatch, capsys: pytest.CaptureFixture[str]
) -> None:
    refused_error = error_class("AccessRefused")("https://example.org/x", 403)
    fake_get(monkeypatch, [("", refused_error)])
    assert main(["ingest", "vdem-ert"]) == 1
    captured = capsys.readouterr()
    assert captured.out == "" and captured.err.strip()
    with cli_db.connect() as connection:
        oks = connection.execute(text("select ok from source_health")).scalars().all()
    assert oks == [False]


@pytest.mark.db
def test_cli_ingest_not_permitted_returns_1_without_fetching(
    cli_db: Engine, monkeypatch: pytest.MonkeyPatch, capsys: pytest.CaptureFixture[str]
) -> None:
    fetcher = fake_get(monkeypatch, geonames_routes())
    assert main(["ingest", "geonames"]) == 1
    assert capsys.readouterr().err.strip()
    assert fetcher.calls == []


@pytest.mark.db
def test_cli_ingest_unknown_source_returns_1(
    cli_db: Engine, capsys: pytest.CaptureFixture[str]
) -> None:
    assert main(["ingest", "no-such-source"]) == 1
    assert "no-such-source" in capsys.readouterr().err


def test_cli_ingest_without_database_url_returns_2(
    monkeypatch: pytest.MonkeyPatch, capsys: pytest.CaptureFixture[str]
) -> None:
    monkeypatch.delenv("CANARY_DATABASE_URL", raising=False)
    assert main(["ingest", "vdem-ert"]) == 2
    assert "CANARY_DATABASE_URL" in capsys.readouterr().err


@pytest.mark.db
def test_cli_health_prints_times_in_utc(cli_db: Engine, capsys: pytest.CaptureFixture[str]) -> None:
    plus_five = datetime.timezone(datetime.timedelta(hours=5))
    with Session(cli_db) as session:
        record_health(
            session,
            "vdem-ert",
            ok=True,
            checked_at=datetime.datetime(2026, 11, 1, 12, 0, tzinfo=plus_five),
        )
        session.commit()
    assert main(["health"]) == 0
    line = next(x for x in capsys.readouterr().out.splitlines() if x.startswith("vdem-ert "))
    assert line.split()[-1] == "2026-11-01T07:00:00+00:00"


# --- review fixes: time ------------------------------------------------------


def one(session: Session, sql: str, **params: Any) -> Any:
    return scalar(session, sql, **params)


def stamp(session: Session) -> datetime.datetime:
    """The newest retrieved_at among observations: when Canary last came to hold a value."""
    return one(session, "select max(retrieved_at) from observation")


def last_run_start(session: Session) -> datetime.datetime:
    return one(session, "select max(started_at) from pipeline_run where config_digest <> 'seed'")


def sums(session: Session, indicator: str, as_of: datetime.datetime) -> dict[Any, float]:
    return {
        (o.geo_ref, o.period_start): o.value for o in observations_as_of(session, indicator, as_of)
    }


@pytest.mark.db
def test_country_mapped_on_a_reparse_is_absent_before_and_present_after(
    db_session: Session, store: RawStore
) -> None:
    seed_places(db_session)
    register(db_session, "ucdp-candidate")
    adapter = ADAPTERS["ucdp-candidate"]
    ingest(db_session, adapter(), FakeFetcher(candidate_routes()), store)
    t1 = stamp(db_session)
    add_place(db_session, "ATL", "AT", "Atlantis")
    again = ingest(db_session, adapter(), FakeFetcher(candidate_routes()), store)
    t2 = last_run_start(db_session)
    assert again.new_release is False and again.written == 2 and again.unmapped == 0
    jan = datetime.date(2026, 1, 1)
    assert ("ATL", jan) not in sums(db_session, "ucdp-candidate-events", t1)
    assert sums(db_session, "ucdp-candidate-events", t2)[("ATL", jan)] == 1.0
    assert sums(db_session, "ucdp-candidate-deaths", t2)[("ATL", jan)] == 9.0
    assert t2 > t1


@pytest.mark.db
def test_alias_onto_an_existing_code_writes_a_new_vintage_for_the_changed_months(
    db_session: Session, store: RawStore, monkeypatch: pytest.MonkeyPatch
) -> None:
    seed_places(db_session)
    register(db_session, "ucdp-candidate")
    adapter = ADAPTERS["ucdp-candidate"]
    ingest(db_session, adapter(), FakeFetcher(candidate_routes()), store)
    t1 = stamp(db_session)
    monkeypatch.setattr(canary.geo, "load_aliases", lambda *a, **k: {"Atlantis": "GHA"})
    again = ingest(db_session, adapter(), FakeFetcher(candidate_routes()), store)
    t2 = last_run_start(db_session)
    jan, feb = datetime.date(2026, 1, 1), datetime.date(2026, 2, 1)
    assert (again.new_release, again.written, again.unmapped) == (False, 2, 0)
    assert sums(db_session, "ucdp-candidate-events", t1)[("GHA", jan)] == 2.0
    assert sums(db_session, "ucdp-candidate-deaths", t1)[("GHA", jan)] == 8.0
    assert sums(db_session, "ucdp-candidate-events", t2)[("GHA", jan)] == 3.0
    assert sums(db_session, "ucdp-candidate-deaths", t2)[("GHA", jan)] == 17.0
    assert sums(db_session, "ucdp-candidate-events", t2)[("GHA", feb)] == 1.0
    assert (
        one(
            db_session,
            "select count(*) from observation where geo_ref = 'GHA' "
            "and period_start = '2026-02-01' and indicator_id = 'ucdp-candidate-events'",
        )
        == 1
    )


@pytest.mark.db
def test_releases_a_b_a_through_the_runner(db_session: Session, store: RawStore) -> None:
    seed_places(db_session)
    register(db_session, "vdem-ert")

    def run(version: str, value: str) -> Any:
        routes = ert_variant_routes(version, value)
        return ingest(db_session, ADAPTERS["vdem-ert"](), FakeFetcher(routes), store)

    jan = datetime.date(2020, 1, 1)

    def ghana(at: datetime.datetime) -> float:
        return sums(db_session, "ert-aut-ep", at)[("GHA", jan)]

    first = run("15.0.1", "0")
    t1 = stamp(db_session)
    second = run("15.0.2", "1")
    t2 = stamp(db_session)
    third = run("15.0.1", "0")
    t3 = last_run_start(db_session)
    fourth = run("15.0.1", "0")
    assert (first.new_release, second.new_release, third.new_release) == (True, True, False)
    assert (first.written, second.written, third.written, fourth.written) == (7, 1, 1, 0)
    assert (ghana(t1), ghana(t2), ghana(t3)) == (0.0, 1.0, 0.0)
    assert t1 < t2 < t3
    newest = [o for o in observations_as_of(db_session, "ert-aut-ep", t3) if o.geo_ref == "GHA"][0]
    release_a = one(db_session, "select id from dataset_release where version_label = '15.0.1'")
    assert (newest.vintage_release_id, newest.retrieved_at) == (release_a, t3)
    assert one(db_session, "select count(*) from observation") == 9


# --- review fixes: tracing ---------------------------------------------------


def geonames_bytes(name: str = "Ghana") -> bytes:
    return fixture("geonames", "countryInfo.txt").replace(b"\tGhana\t", f"\t{name}\t".encode())


def run_geonames(session: Session, store: RawStore, data: bytes) -> Any:
    return ingest(session, ADAPTERS["geonames"](), FakeFetcher([("countryInfo.txt", data)]), store)


def versions(session: Session) -> dict[str, list[int]]:
    out: dict[str, list[int]] = {}
    for pid, version in session.execute(
        text("select place_id, version from place_version order by 1, 2")
    ):
        out.setdefault(pid, []).append(version)
    return out


@pytest.mark.db
def test_geonames_ingest_writes_version_one_for_every_place(
    db_session: Session, store: RawStore
) -> None:
    register(db_session, "geonames")
    run_geonames(db_session, store, geonames_bytes())
    assert versions(db_session) == {"GHA": [1], "MLI": [1], "NER": [1]}
    assert one(db_session, "select count(*) from place where current_version = 1") == 3
    run_id = one(db_session, "select run_id from place where id = 'GHA'")
    assert run_id == one(db_session, "select run_id from place_version where place_id = 'GHA'")


@pytest.mark.db
def test_second_identical_geonames_ingest_writes_nothing(
    db_session: Session, store: RawStore
) -> None:
    register(db_session, "geonames")
    run_geonames(db_session, store, geonames_bytes())
    first_run = one(db_session, "select run_id from place where id = 'GHA'")
    run_geonames(db_session, store, geonames_bytes())
    assert versions(db_session) == {"GHA": [1], "MLI": [1], "NER": [1]}
    assert one(db_session, "select run_id from place where id = 'GHA'") == first_run


@pytest.mark.db
def test_a_changed_place_name_writes_version_two_for_that_place_only(
    db_session: Session, store: RawStore
) -> None:
    register(db_session, "geonames")
    run_geonames(db_session, store, geonames_bytes())
    run_geonames(db_session, store, geonames_bytes("Republic of Ghana"))
    assert versions(db_session) == {"GHA": [1, 2], "MLI": [1], "NER": [1]}
    row = db_session.execute(
        text("select name, current_version, run_id from place where id = 'GHA'")
    ).one()
    assert (row.name, row.current_version) == ("Republic of Ghana", 2)
    newest = db_session.execute(
        text("select record, run_id from place_version where place_id = 'GHA' and version = 2")
    ).one()
    assert newest.record["name"] == "Republic of Ghana"
    assert newest.run_id == row.run_id


@pytest.mark.db
def test_wikidata_link_adds_wikidata_id_keeps_other_fields_and_writes_a_version(
    db_session: Session, store: RawStore
) -> None:
    register(db_session, "geonames")
    register(db_session, "wikidata")
    run_geonames(db_session, store, geonames_bytes())
    before = one(db_session, "select record from place_version where place_id = 'GHA'")
    wd = FakeFetcher(wikidata_routes())
    ingest(db_session, ADAPTERS["wikidata"](), wd, store)
    assert versions(db_session) == {"GHA": [1, 2], "MLI": [1, 2], "NER": [1]}
    after = one(
        db_session, "select record from place_version where place_id = 'GHA' and version = 2"
    )
    assert after["wikidata_id"] == "Q117"
    assert {k: v for k, v in after.items() if k != "wikidata_id"} == {
        k: v for k, v in before.items() if k != "wikidata_id"
    }
    assert one(db_session, "select wikidata_id from place where id = 'GHA'") == "Q117"
    assert one(db_session, "select name from place where id = 'GHA'") == "Ghana"
    ingest(db_session, ADAPTERS["wikidata"](), FakeFetcher(wikidata_routes()), store)
    assert versions(db_session) == {"GHA": [1, 2], "MLI": [1, 2], "NER": [1]}


@pytest.mark.db
@pytest.mark.parametrize(
    "sql",
    [
        "update place_version set digest = 'x'",
        "delete from place_version",
        "truncate place_version",
    ],
)
def test_place_version_refuses_update_delete_and_truncate(db_session: Session, sql: str) -> None:
    seed_places(db_session)
    refused(db_session, sql)
    assert scalar(db_session, "select count(*) from place_version") == 3


@pytest.mark.db
def test_resolver_digest_never_raises_and_changes_with_a_place_name(db_session: Session) -> None:
    empty = canary.geo.resolver_digest(db_session)
    assert len(empty) == 64
    seed_places(db_session)
    full = canary.geo.resolver_digest(db_session)
    assert full != empty and canary.geo.resolver_digest(db_session) == full
    db_session.execute(text("update place set name = 'Gold Coast' where id = 'GHA'"))
    assert canary.geo.resolver_digest(db_session) not in (empty, full)


@pytest.mark.db
def test_run_config_digest_includes_the_resolver_only_for_resolver_adapters(
    db_session: Session, store: RawStore
) -> None:
    seed_places(db_session)
    register(db_session, "vdem-ert")
    register(db_session, "ucdp-candidate")

    def digests() -> list[str]:
        return [
            r.config_digest
            for r in db_session.execute(
                text(
                    "select config_digest from pipeline_run where config_digest <> 'seed' "
                    "order by started_at"
                )
            )
        ]

    ingest(db_session, ADAPTERS["vdem-ert"](), FakeFetcher(ert_routes()), store)
    ingest(db_session, ADAPTERS["ucdp-candidate"](), FakeFetcher(candidate_routes()), store)
    db_session.execute(text("update place set name = 'Gold Coast' where id = 'GHA'"))
    ingest(db_session, ADAPTERS["vdem-ert"](), FakeFetcher(ert_routes()), store)
    ingest(db_session, ADAPTERS["ucdp-candidate"](), FakeFetcher(candidate_routes()), store)
    ert1, ucdp1, ert2, ucdp2 = digests()
    assert ert1 == ert2 == ADAPTERS["vdem-ert"]().config_digest()
    assert ucdp1 != ADAPTERS["ucdp-candidate"]().config_digest()
    assert ucdp1 != ucdp2


@pytest.mark.db
def test_unmapped_names_are_recorded_in_the_health_message_and_ok_stays_true(
    db_session: Session, store: RawStore
) -> None:
    seed_places(db_session)
    register(db_session, "ucdp-candidate")
    ingest(db_session, ADAPTERS["ucdp-candidate"](), FakeFetcher(candidate_routes()), store)
    health = db_session.execute(text("select ok, message from source_health")).one()
    assert (health.ok, health.message) == (True, "unmapped: 1")


@pytest.mark.db
def test_file_refs_carry_the_url_each_file_came_from(db_session: Session, store: RawStore) -> None:
    seed_places(db_session)
    register(db_session, "vdem-ert")
    ingest_ert(db_session, store)
    refs = one(db_session, "select file_refs from dataset_release")
    by_name = {r["filename"]: r for r in refs}
    assert by_name["ert.csv"]["url"].endswith("inst/ert.csv")
    assert all(r["url"].startswith("https://") for r in refs)
