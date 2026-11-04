"""Dataset adapters against fixtures (real headers, invented rows). No network, no db."""

from __future__ import annotations

import datetime
import hashlib
import pathlib
import re
import shutil
import struct
import sys
import zipfile
from collections.abc import Callable
from typing import Any

import pytest

from canary.adapters import ADAPTERS
from canary.adapters.base import highest_link, only_csv_in_zip, page_link
from canary.errors import AccessRefused, FetchFailed
from canary.geo import CountryResolver
from canary.rawstore import RawStore
from fixtures.ingest_support import (
    FakeFetcher,
    acd_routes,
    candidate_routes,
    error_class,
    ert_routes,
    ewp_routes,
    fixture,
    ged_routes,
    geonames_routes,
    is_page,
    row_set,
    run_pipeline,
    wb_routes,
    wikidata_routes,
)

D = datetime.date


def year(y: int) -> tuple[D, D]:
    return D(y, 1, 1), D(y, 12, 31)


def month(y: int, m: int, last: int) -> tuple[D, D]:
    return D(y, m, 1), D(y, m, last)


@pytest.fixture
def resolver() -> CountryResolver:
    return CountryResolver({"Ghana": "GHA", "Mali": "MLI", "Niger": "NER"}, {})


@pytest.fixture
def store(tmp_path: pathlib.Path) -> RawStore:
    return RawStore(tmp_path / "raw")


def adapter(source_id: str) -> Any:
    return ADAPTERS[source_id]()


def go(source_id: str, routes: list[Any], store: RawStore, resolver: Any) -> tuple[Any, Any]:
    return run_pipeline(adapter(source_id), FakeFetcher(routes), store, resolver)


def directions(result: Any) -> dict[str, str]:
    return {i.id: i.deterioration_direction for i in result.indicators}


def sha12(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()[:12]


def test_adapters_table_covers_every_source_in_the_contract() -> None:
    expected = {
        "vdem-country-year", "vdem-ert", "ucdp-candidate", "ucdp-ged", "ucdp-prio-acd",
        "world-bank-indicators", "our-world-in-data", "ewp-sra", "cline-coups", "geonames",
        "wikidata", "natural-earth",
    }  # fmt: skip
    assert set(ADAPTERS) == expected
    for source_id in expected:
        a = adapter(source_id)
        assert a.source_id == source_id
        assert len(a.config_digest()) > 0


# --- V-Dem -----------------------------------------------------------------

VDEM = [
    "v2x_polyarchy", "v2x_libdem", "v2x_partipdem", "v2x_delibdem", "v2x_egaldem", "v2x_jucon",
    "v2xlg_legcon", "v2x_freexp_altinf", "v2x_frassoc_thick", "v2xcl_rol", "v2x_cspart",
    "v2x_civlib", "v2x_clphy", "v2xel_frefair", "v2x_corr",
]  # fmt: skip


def vdem_record(code: str, y: int, **overrides: Any) -> dict[str, Any]:
    rec: dict[str, Any] = {"country_text_id": code, "year": y}
    for column in VDEM:
        rec[column] = 0.5
        rec[column + "_codelow"] = 0.4
        rec[column + "_codehigh"] = 0.6
    rec.update(overrides)
    return rec


CODEBOOK = {c: {"name": f"Name of {c}", "definition": f"Definition of {c}"} for c in VDEM}


def rows_from_records() -> Callable[..., Any]:
    module = sys.modules[type(adapter("vdem-country-year")).__module__]
    return module.rows_from_records  # type: ignore[no-any-return]


def test_vdem_discover_label_is_the_description_version(store: RawStore) -> None:
    routes = [("vdemdata/master/DESCRIPTION", fixture("vdem-country-year", "DESCRIPTION"))]
    assert adapter("vdem-country-year").discover(FakeFetcher(routes)).version_label == "15.0"


def test_vdem_fetch_stores_the_data_and_codebook_files(store: RawStore) -> None:
    routes = [
        ("vdemdata/master/DESCRIPTION", fixture("vdem-country-year", "DESCRIPTION")),
        ("data/vdem.RData", b"data-bytes"),
        ("data/codebook.RData", b"codebook-bytes"),
    ]
    fetcher = FakeFetcher(routes)
    a = adapter("vdem-country-year")
    refs = a.fetch(fetcher, a.discover(fetcher), store)
    expected = sorted([len(b"codebook-bytes"), len(b"data-bytes")])
    assert sorted(r.size_bytes for r in refs) == expected


def test_vdem_records_become_one_indicator_per_column_with_bounds() -> None:
    result = rows_from_records()([vdem_record("GHA", 2020, v2x_polyarchy=0.7)], CODEBOOK)
    assert {i.id for i in result.indicators} == {f"vdem-{c}" for c in VDEM}
    start, end = year(2020)
    assert ("vdem-v2x_polyarchy", "GHA", start, end, 0.7, 0.4, 0.6) in row_set(result)
    assert len(result.rows) == 15
    by_id = {i.id: i for i in result.indicators}
    assert by_id["vdem-v2x_polyarchy"].name == "Name of v2x_polyarchy"
    assert by_id["vdem-v2x_polyarchy"].definition == "Definition of v2x_polyarchy"


def test_vdem_direction_is_down_except_corruption() -> None:
    result = rows_from_records()([vdem_record("GHA", 2020)], CODEBOOK)
    expected = {f"vdem-{c}": "down" for c in VDEM}
    expected["vdem-v2x_corr"] = "up"
    assert directions(result) == expected


@pytest.mark.parametrize("blank", [None, "NA", ""])
def test_vdem_blank_values_are_left_out_not_counted_as_skipped(blank: Any) -> None:
    result = rows_from_records()([vdem_record("GHA", 2020, v2x_libdem=blank)], CODEBOOK)
    assert not [r for r in result.rows if r.indicator_id == "vdem-v2x_libdem"]
    assert len(result.rows) == 14
    assert result.skipped == 0


def test_vdem_historical_entities_keep_their_own_code() -> None:
    result = rows_from_records()([vdem_record("DDR", 1980)], CODEBOOK)
    assert {r.geo_ref for r in result.rows} == {"DDR"}
    assert result.skipped == 0


def test_vdem_codebook_missing_a_column_raises_schema_changed() -> None:
    codebook = {k: v for k, v in CODEBOOK.items() if k != "v2x_corr"}
    with pytest.raises(error_class("SchemaChanged"), match="v2x_corr"):
        rows_from_records()([vdem_record("GHA", 2020)], codebook)


def test_vdem_record_missing_a_column_raises_schema_changed_naming_it() -> None:
    record = vdem_record("GHA", 2020)
    del record["v2x_cspart_codehigh"]
    with pytest.raises(error_class("SchemaChanged"), match="v2x_cspart_codehigh"):
        rows_from_records()([record], CODEBOOK)


# --- V-Dem ERT -------------------------------------------------------------


def test_ert_discover_label_and_parse(store: RawStore, resolver: Any) -> None:
    ref, result = go("vdem-ert", ert_routes(), store, resolver)
    assert ref.version_label == "15.0.1"
    a20, a21 = year(2020), year(2021)
    assert row_set(result) == {
        ("ert-aut-ep", "GHA", *a20, 0.0, None, None),
        ("ert-aut-ep", "GHA", *a21, 0.0, None, None),
        ("ert-aut-ep", "MLI", *a20, 1.0, None, None),
        ("ert-dem-ep", "GHA", *a20, 1.0, None, None),
        ("ert-dem-ep", "GHA", *a21, 0.0, None, None),
        ("ert-dem-ep", "MLI", *a20, 0.0, None, None),
        ("ert-dem-ep", "MLI", *a21, 0.0, None, None),
    }
    assert directions(result) == {"ert-aut-ep": "up", "ert-dem-ep": "none"}
    assert (result.skipped, result.unmapped) == (0, [])
    assert len(result.schema_digest) == 64


# --- UCDP candidate and GED ------------------------------------------------

JAN, FEB = month(2026, 1, 31), month(2026, 2, 28)


def ucdp_expected(prefix: str) -> set[tuple[Any, ...]]:
    return {
        (f"{prefix}-events", "GHA", *JAN, 2.0, None, None),
        (f"{prefix}-events", "GHA", *FEB, 1.0, None, None),
        (f"{prefix}-events", "MLI", *JAN, 1.0, None, None),
        (f"{prefix}-deaths", "GHA", *JAN, 8.0, 6.0, 11.0),
        (f"{prefix}-deaths", "GHA", *FEB, 1.0, 1.0, 1.0),
        (f"{prefix}-deaths", "MLI", *JAN, 0.0, 0.0, 0.0),
    }


def test_candidate_discover_takes_the_highest_numeric_version(store: RawStore) -> None:
    ref = adapter("ucdp-candidate").discover(FakeFetcher(candidate_routes()))
    assert "26_01_26_09" in ref.version_label
    assert len(ref.urls) == 1
    assert next(iter(ref.urls.values())).endswith("GEDEvent_v26_01_26_09.csv")


def test_candidate_discover_falls_back_to_the_zero_pattern(store: RawStore) -> None:
    page = fixture("ucdp-candidate", "downloads_fallback.html")
    ref = adapter("ucdp-candidate").discover(FakeFetcher([(is_page, page)]))
    assert "26_0_9" in ref.version_label
    assert next(iter(ref.urls.values())).endswith("GEDEvent_v26_0_9.csv")


def test_candidate_parse_sums_events_and_deaths_by_month(store: RawStore, resolver: Any) -> None:
    _, result = go("ucdp-candidate", candidate_routes(), store, resolver)
    assert row_set(result) == ucdp_expected("ucdp-candidate")
    assert result.skipped == 1
    assert result.unmapped == ["Atlantis"]
    assert "preliminary" in {i.reporting_bias_note for i in result.indicators}.pop().lower()


def test_ged_discover_takes_the_highest_zip_and_parse_reads_its_csv(
    store: RawStore, resolver: Any
) -> None:
    ref, result = go("ucdp-ged", ged_routes(), store, resolver)
    assert next(iter(ref.urls.values())).endswith("ged261-csv.zip")
    assert row_set(result) == ucdp_expected("ucdp-ged")
    assert result.unmapped == ["Atlantis"]


# --- UCDP/PRIO ACD ---------------------------------------------------------


def test_acd_splits_multi_country_location_and_keeps_zero_war_counts(
    store: RawStore, resolver: Any
) -> None:
    ref, result = go("ucdp-prio-acd", acd_routes(), store, resolver)
    assert next(iter(ref.urls.values())).endswith("ucdp-prio-acd-261-csv.zip")
    y20, y21 = year(2020), year(2021)
    assert row_set(result) == {
        ("acd-active-conflicts", "GHA", *y20, 2.0, None, None),
        ("acd-war-conflicts", "GHA", *y20, 1.0, None, None),
        ("acd-active-conflicts", "MLI", *y20, 1.0, None, None),
        ("acd-war-conflicts", "MLI", *y20, 0.0, None, None),
        ("acd-active-conflicts", "MLI", *y21, 2.0, None, None),
        ("acd-war-conflicts", "MLI", *y21, 0.0, None, None),
    }
    assert result.unmapped == ["Atlantis"]


# --- World Bank ------------------------------------------------------------


def test_world_bank_follows_pages_drops_aggregates_and_empty_codes(
    store: RawStore, resolver: Any
) -> None:
    fetcher = FakeFetcher(wb_routes())
    a = adapter("world-bank-indicators")
    ref = a.discover(fetcher)
    result = a.parse(a.fetch(fetcher, ref, store), resolver)
    assert ref.version_label == "2026-10-15"
    y = year(2020)
    assert row_set(result) == {
        ("wb-FP.CPI.TOTL.ZG", "GHA", *y, 9.9, None, None),
        ("wb-FP.CPI.TOTL.ZG", "MLI", *y, 1.5, None, None),
        ("wb-NY.GDP.PCAP.KD.ZG", "GHA", *y, 0.5, None, None),
        ("wb-SL.UEM.TOTL.ZS", "GHA", *y, 4.2, None, None),
        ("wb-SP.POP.TOTL", "GHA", *y, 31072945.0, None, None),
    }
    assert result.skipped == 2
    assert any("page=2" in call for call in fetcher.calls)
    assert directions(result) == {
        "wb-FP.CPI.TOTL.ZG": "up",
        "wb-NY.GDP.PCAP.KD.ZG": "down",
        "wb-SL.UEM.TOTL.ZS": "up",
        "wb-SP.POP.TOTL": "none",
    }


# --- Our World in Data -----------------------------------------------------

OWID_ROUTES = [
    (
        "life-expectancy.metadata.json",
        fixture("our-world-in-data", "life-expectancy.metadata.json"),
    ),
    ("life-expectancy.csv", fixture("our-world-in-data", "life-expectancy.csv")),
]


def test_owid_default_allow_list_is_empty() -> None:
    module = sys.modules[type(adapter("our-world-in-data")).__module__]
    assert list(module.SERIES) == []


def test_owid_injected_slug_parses_normally(store: RawStore, resolver: Any) -> None:
    injected = type(adapter("our-world-in-data"))(["life-expectancy"])
    ref, result = run_pipeline(injected, FakeFetcher(OWID_ROUTES), store, resolver)
    assert ref.version_label == "2026-09-01"
    indicator = "owid-life-expectancy-life_expectancy_0"
    assert row_set(result) == {
        (indicator, "AFG", *year(1950), 28.1563, None, None),
        (indicator, "GHA", *year(1951), 40.0, None, None),
    }


# --- EWP -------------------------------------------------------------------


def test_ewp_period_comes_from_the_column_name_and_values_are_unchanged(
    store: RawStore, resolver: Any
) -> None:
    ref, result = go("ewp-sra", ewp_routes(), store, resolver)
    assert ref.version_label == f"{datetime.date.today().year}-sra"
    start, end = D(2025, 1, 1), D(2026, 12, 31)
    assert row_set(result) == {
        ("ewp-sra-risk", "GHA", start, end, 0.0123, None, None),
        ("ewp-sra-risk", "MLI", start, end, 0.0456, None, None),
        ("ewp-sra-rank", "GHA", start, end, 41.0, None, None),
        ("ewp-sra-rank", "MLI", start, end, 12.0, None, None),
        ("ewp-sra-rank", "NER", start, end, 77.0, None, None),
    }
    assert directions(result) == {"ewp-sra-risk": "up", "ewp-sra-rank": "none"}


# --- Cline -----------------------------------------------------------------


def drop(tmp_path: pathlib.Path, monkeypatch: pytest.MonkeyPatch, files: dict[str, str]) -> None:
    folder = tmp_path / "drop"
    (folder / "cline-coups").mkdir(parents=True)
    for name, source in files.items():
        shutil.copy(
            pathlib.Path(__file__).parent / "fixtures" / "cline-coups" / source,
            folder / "cline-coups" / name,
        )
    monkeypatch.setenv("CANARY_DROP_DIR", str(folder))


def test_cline_one_file_sums_flags_per_country_and_year(
    tmp_path: pathlib.Path, monkeypatch: pytest.MonkeyPatch, store: RawStore, resolver: Any
) -> None:
    drop(tmp_path, monkeypatch, {"cline_coups_2.2.2.csv": "cline_coups_2.2.2.csv"})
    ref, result = go("cline-coups", [], store, resolver)
    assert "2.2.2" in ref.version_label
    r79, r81, r68 = year(1979), year(1981), year(1968)
    assert row_set(result) == {
        ("cline-realized", "GHA", *r79, 1.0, None, None),
        ("cline-attempts", "GHA", *r79, 1.0, None, None),
        ("cline-conspiracies", "GHA", *r79, 1.0, None, None),
        ("cline-realized", "GHA", *r81, 1.0, None, None),
        ("cline-attempts", "GHA", *r81, 0.0, None, None),
        ("cline-conspiracies", "GHA", *r81, 0.0, None, None),
        ("cline-realized", "MLI", *r68, 1.0, None, None),
        ("cline-attempts", "MLI", *r68, 0.0, None, None),
        ("cline-conspiracies", "MLI", *r68, 0.0, None, None),
    }
    assert result.skipped == 1
    assert result.unmapped == ["Atlantis"]


def test_cline_label_is_unknown_when_the_name_carries_no_version(
    tmp_path: pathlib.Path, monkeypatch: pytest.MonkeyPatch, store: RawStore, resolver: Any
) -> None:
    drop(tmp_path, monkeypatch, {"coups.csv": "cline_coups_2.2.2.csv"})
    ref, _ = go("cline-coups", [], store, resolver)
    assert ref.version_label == "unknown"


def test_cline_no_file_raises_manual_file_missing_naming_the_folder(
    tmp_path: pathlib.Path, monkeypatch: pytest.MonkeyPatch, store: RawStore, resolver: Any
) -> None:
    drop(tmp_path, monkeypatch, {})
    with pytest.raises(error_class("ManualFileMissing"), match="cline-coups"):
        go("cline-coups", [], store, resolver)


def test_cline_two_files_raise_manual_file_missing(
    tmp_path: pathlib.Path, monkeypatch: pytest.MonkeyPatch, store: RawStore, resolver: Any
) -> None:
    drop(
        tmp_path, monkeypatch, {"a.csv": "cline_coups_2.2.2.csv", "b.csv": "cline_coups_2.2.2.csv"}
    )
    with pytest.raises(error_class("ManualFileMissing")):
        go("cline-coups", [], store, resolver)


# --- GeoNames, Wikidata, Natural Earth -------------------------------------


def test_geonames_yields_places_only_and_labels_by_file_hash(
    store: RawStore, resolver: Any
) -> None:
    ref, result = go("geonames", geonames_routes(), store, resolver)
    assert ref.version_label == sha12(fixture("geonames", "countryInfo.txt"))
    assert result.rows == [] and len(result.places) == 3


def test_wikidata_label_is_the_file_hash(store: RawStore, resolver: Any) -> None:
    ref, result = go("wikidata", wikidata_routes(), store, resolver)
    assert ref.version_label == sha12(fixture("wikidata", "iso3.csv"))
    assert result.rows == []


def test_natural_earth_keeps_the_file_and_yields_no_rows(store: RawStore, resolver: Any) -> None:
    data = fixture("natural-earth", "ne_50m_admin_0_countries.zip")
    routes = [("naciscdn.org/naturalearth/50m/cultural/ne_50m_admin_0_countries.zip", data)]
    fetcher = FakeFetcher(routes)
    ref, result = run_pipeline(adapter("natural-earth"), fetcher, store, resolver)
    assert ref.version_label == sha12(data)
    assert result.rows == [] and result.indicators == []
    assert len(fetcher.calls) == 1 and fetcher.calls[0].startswith("https://naciscdn.org/")


# --- Changed schemas -------------------------------------------------------


def changed_cases(tmp_path: pathlib.Path, monkeypatch: pytest.MonkeyPatch) -> dict[str, Any]:
    def owid() -> Any:
        routes = [
            (
                "life-expectancy.metadata.json",
                fixture("our-world-in-data", "life-expectancy.metadata.json"),
            ),
            ("life-expectancy.csv", fixture("our-world-in-data", "life-expectancy_changed.csv")),
        ]
        return type(adapter("our-world-in-data"))(["life-expectancy"]), routes

    def cline() -> Any:
        drop(tmp_path, monkeypatch, {"cline_coups_2.2.2.csv": "cline_coups_2.2.2_changed.csv"})
        return adapter("cline-coups"), []

    def plain(source_id: str, routes: list[Any]) -> Callable[[], Any]:
        return lambda: (adapter(source_id), routes)

    return {
        "vdem-ert": plain("vdem-ert", ert_routes(changed=True)),
        "ucdp-candidate": plain("ucdp-candidate", candidate_routes(changed=True)),
        "ucdp-ged": plain("ucdp-ged", ged_routes(changed=True)),
        "ucdp-prio-acd": plain("ucdp-prio-acd", acd_routes(changed=True)),
        "world-bank-indicators": plain("world-bank-indicators", wb_routes(changed=True)),
        "ewp-sra": plain("ewp-sra", ewp_routes(changed=True)),
        "geonames": plain("geonames", geonames_routes(changed=True)),
        "wikidata": plain("wikidata", wikidata_routes(changed=True)),
        "our-world-in-data": owid,
        "cline-coups": cline,
    }


CHANGED = [
    "vdem-ert", "ucdp-candidate", "ucdp-ged", "ucdp-prio-acd", "world-bank-indicators",
    "ewp-sra", "geonames", "wikidata", "our-world-in-data", "cline-coups",
]  # fmt: skip


@pytest.mark.parametrize("source_id", CHANGED)
def test_changed_schema_raises_schema_changed_and_yields_no_partial_result(
    source_id: str,
    tmp_path: pathlib.Path,
    monkeypatch: pytest.MonkeyPatch,
    store: RawStore,
    resolver: Any,
) -> None:
    a, routes = changed_cases(tmp_path, monkeypatch)[source_id]()
    with pytest.raises(error_class("SchemaChanged")):
        run_pipeline(a, FakeFetcher(routes), store, resolver)


def test_ewp_probes_from_next_year_down_and_takes_the_first_file_that_exists(
    store: RawStore,
) -> None:
    fetcher = FakeFetcher(ewp_routes())
    a = adapter("ewp-sra")
    ref = a.discover(fetcher)
    year = datetime.date.today().year
    assert ref.version_label == f"{year}-sra"
    assert [c.rsplit("/", 1)[-1] for c in fetcher.calls[:2]] == [f"{year + 1}-sra", f"{year}-sra"]
    assert list(ref.urls) == [f"{year}-sra"]


def test_ewp_with_no_file_in_the_probed_years_fails_as_a_fetch_failure() -> None:
    fetcher = FakeFetcher(
        [(re.compile(r"api/sra/download/csv/\d{4}-sra"), FetchFailed("HTTP 404"))]
    )
    with pytest.raises(FetchFailed):
        adapter("ewp-sra").discover(fetcher)


def test_ewp_access_refused_is_not_treated_as_a_missing_year() -> None:
    refused = AccessRefused("https://example.org/x", 403)
    fetcher = FakeFetcher([(re.compile(r"api/sra/download/csv/\d{4}-sra"), refused)])
    with pytest.raises(AccessRefused):
        adapter("ewp-sra").discover(fetcher)
    assert len(fetcher.calls) == 1


# --- review fixes: links stay on the page's host, zip members are bounded -----

PATTERN = re.compile(r"/ged(\d+)-csv\.zip$")
PAGE_URL = "https://example.org/downloads/"


def page(*hrefs: str) -> bytes:
    return "".join(f'<a href="{h}">x</a>' for h in hrefs).encode()


def test_page_link_ignores_another_host_even_when_the_path_matches() -> None:
    html = page(
        "https://evil.example.net/ged999-csv.zip", "https://example.org/files/ged261-csv.zip"
    )
    url, match = page_link(html, PAGE_URL, PATTERN)
    assert url == "https://example.org/files/ged261-csv.zip" and match.group(1) == "261"


def test_page_link_ignores_file_links_even_when_the_path_matches(tmp_path: pathlib.Path) -> None:
    html = page((tmp_path / "ged999-csv.zip").as_uri(), "/files/ged261-csv.zip")
    url, _ = page_link(html, PAGE_URL, PATTERN)
    assert url == "https://example.org/files/ged261-csv.zip"


def test_page_link_accepts_http_and_relative_links_on_the_same_host() -> None:
    assert page_link(page("http://example.org/a/ged5-csv.zip"), PAGE_URL, PATTERN) is not None
    assert page_link(page("ged6-csv.zip"), PAGE_URL, PATTERN) is not None


def test_page_link_with_only_foreign_links_finds_nothing_and_highest_link_raises(
    tmp_path: pathlib.Path,
) -> None:
    html = page("https://example.org.evil.net/ged1-csv.zip", (tmp_path / "ged2-csv.zip").as_uri())
    assert page_link(html, PAGE_URL, PATTERN) is None
    with pytest.raises(error_class("SchemaChanged")):
        highest_link(html, PAGE_URL, PATTERN)


def zip_declaring(size: int, tmp_path: pathlib.Path) -> bytes:
    path = tmp_path / "small.zip"
    with zipfile.ZipFile(path, "w") as archive:
        archive.writestr("data.csv", "a,b\n1,2\n")
    data = bytearray(path.read_bytes())
    central = data.index(b"PK\x01\x02")
    data[central + 24 : central + 28] = struct.pack("<I", size)
    return bytes(data)


def test_zip_member_declaring_over_2_gb_is_refused_before_reading(
    tmp_path: pathlib.Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    def must_not_read(*args: Any, **kwargs: Any) -> bytes:
        raise AssertionError("the member was read")

    declared = zip_declaring(2_500_000_000, tmp_path)
    monkeypatch.setattr(zipfile.ZipFile, "read", must_not_read)
    monkeypatch.setattr(zipfile.ZipFile, "open", must_not_read)
    with pytest.raises(error_class("SchemaChanged")):
        only_csv_in_zip(declared)
