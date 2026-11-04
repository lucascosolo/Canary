"""Shared helpers for the ingestion tests: fixture reading, a recording fake fetcher, db seeding."""

from __future__ import annotations

import datetime
import importlib
import pathlib
import re
import uuid
from collections.abc import Callable
from typing import Any
from urllib.parse import urlencode

from sqlalchemy import text
from sqlalchemy.orm import Session

from canary.provenance import start_run, sync_registry
from canary.registry import SourceEntry

FIXTURES = pathlib.Path(__file__).parent
ERROR_MODULES = ("canary.errors", "canary.ingest", "canary.http", "canary.rawstore", "canary.geo")


def fixture(source_id: str, name: str) -> bytes:
    return (FIXTURES / source_id / name).read_bytes()


def error_class(name: str) -> type[Exception]:
    """Find an exception class where the implementation put it (the contract names no module)."""
    for module_name in ERROR_MODULES:
        try:
            module = importlib.import_module(module_name)
        except ImportError:
            continue
        if hasattr(module, name):
            return getattr(module, name)
    raise ImportError(f"{name} not found in any of {ERROR_MODULES}")


Route = tuple[str | re.Pattern[str] | Callable[[str], bool], bytes | Exception]


class FakeFetcher:
    """Answers from an ordered route list (first match wins) and records every request."""

    def __init__(self, routes: list[Route]) -> None:
        self.routes = routes
        self.calls: list[str] = []

    def get(self, url: str, *, params: Any = None, headers: Any = None, **kwargs: Any) -> bytes:
        full = url + (("&" if "?" in url else "?") + urlencode(params) if params else "")
        self.calls.append(full)
        for key, answer in self.routes:
            if callable(key):
                hit = key(full)
            elif isinstance(key, re.Pattern):
                hit = key.search(full) is not None
            else:
                hit = key in full
            if hit:
                if isinstance(answer, Exception):
                    raise answer
                return answer
        raise AssertionError(f"unexpected request: {full}")


def is_page(url: str) -> bool:
    return not url.split("?")[0].endswith((".csv", ".zip", ".xlsx"))


def make_entry(source_id: str, canary_use: str = "open") -> SourceEntry:
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
        "canary_use": canary_use,
        "attribution_text": "Example Org",
        "source_class": "intergovernmental",
        "status": "lead",
    }
    return SourceEntry.model_validate(data, context={"today": datetime.date(2026, 11, 4)})


PLACES = [
    ("GHA", "GH", "Ghana", "AF", 2300660),
    ("MLI", "ML", "Mali", "AF", 2453866),
    ("NER", "NE", "Niger", "AF", 2440476),
]


def seed_places(session: Session) -> None:
    run_id = start_run(session, "ingest", code_commit="seed", config_digest="seed")
    for iso3, iso2, name, continent, geonames_id in PLACES:
        session.execute(
            text(
                "insert into place (id, iso2, name, continent, geonames_id, run_id) "
                "values (:i, :i2, :n, :c, :g, :r)"
            ),
            {"i": iso3, "i2": iso2, "n": name, "c": continent, "g": geonames_id, "r": run_id},
        )


def register(session: Session, source_id: str, canary_use: str = "open") -> None:
    run_id = start_run(session, "ingest", code_commit="seed", config_digest="seed")
    sync_registry(session, [make_entry(source_id, canary_use)], run_id=run_id)


def scalar(session: Session, sql: str, **params: Any) -> Any:
    return session.execute(text(sql), params).scalar_one()


def new_uuid() -> uuid.UUID:
    return uuid.uuid4()


# --- per-source routes -------------------------------------------------------

ERT_BASE = "ert"


def ert_routes(changed: bool = False) -> list[Route]:
    return [
        ("ERT/master/DESCRIPTION", fixture("vdem-ert", "DESCRIPTION")),
        ("inst/ert.csv", fixture("vdem-ert", "ert_changed.csv" if changed else "ert.csv")),
    ]


def geonames_routes(changed: bool = False) -> list[Route]:
    name = "countryInfo_changed.txt" if changed else "countryInfo.txt"
    return [("countryInfo.txt", fixture("geonames", name))]


def candidate_routes(changed: bool = False) -> list[Route]:
    name = "GEDEvent_v26_01_26_09_changed.csv" if changed else "GEDEvent_v26_01_26_09.csv"
    return [
        ("GEDEvent_v26_01_26_09.csv", fixture("ucdp-candidate", name)),
        (is_page, fixture("ucdp-candidate", "downloads.html")),
    ]


def ged_routes(changed: bool = False) -> list[Route]:
    name = "ged261-csv_changed.zip" if changed else "ged261-csv.zip"
    return [
        ("ged261-csv.zip", fixture("ucdp-ged", name)),
        (is_page, fixture("ucdp-ged", "downloads.html")),
    ]


def acd_routes(changed: bool = False) -> list[Route]:
    name = "ucdp-prio-acd-261-csv_changed.zip" if changed else "ucdp-prio-acd-261-csv.zip"
    return [
        ("ucdp-prio-acd-261-csv.zip", fixture("ucdp-prio-acd", name)),
        (is_page, fixture("ucdp-prio-acd", "downloads.html")),
    ]


def wb_routes(changed: bool = False) -> list[Route]:
    wb = "world-bank-indicators"
    first = "FP.CPI.TOTL.ZG.page1_changed.json" if changed else "FP.CPI.TOTL.ZG.page1.json"
    return [
        (re.compile(r"/v2/country\?"), fixture(wb, "country.json")),
        (
            re.compile(r"FP\.CPI\.TOTL\.ZG.*[?&]page=2(&|$)"),
            fixture(wb, "FP.CPI.TOTL.ZG.page2.json"),
        ),
        ("FP.CPI.TOTL.ZG", fixture(wb, first)),
        ("NY.GDP.PCAP.KD.ZG", fixture(wb, "NY.GDP.PCAP.KD.ZG.json")),
        ("SL.UEM.TOTL.ZS", fixture(wb, "SL.UEM.TOTL.ZS.json")),
        ("SP.POP.TOTL", fixture(wb, "SP.POP.TOTL.json")),
    ]


def ewp_routes(changed: bool = False) -> list[Route]:
    name = "sra_changed.csv" if changed else "sra.csv"
    return [
        ("api/sra/download/csv/1043-sra", fixture("ewp-sra", name)),
        ("reports-and-downloads", fixture("ewp-sra", "reports-and-downloads.html")),
    ]


def wikidata_routes(changed: bool = False) -> list[Route]:
    return [
        ("query.wikidata.org", fixture("wikidata", "iso3_changed.csv" if changed else "iso3.csv"))
    ]


def run_pipeline(adapter: Any, fetcher: Any, store: Any, resolver: Any) -> tuple[Any, Any]:
    """discover, fetch and parse without a database; returns (release ref, parse result)."""
    ref = adapter.discover(fetcher)
    refs = adapter.fetch(fetcher, ref, store)
    return ref, adapter.parse(refs, resolver)


def row_set(result: Any) -> set[tuple[Any, ...]]:
    return {
        (
            r.indicator_id,
            r.geo_ref,
            r.period_start,
            r.period_end,
            r.value,
            r.value_low,
            r.value_high,
        )
        for r in result.rows
    }
