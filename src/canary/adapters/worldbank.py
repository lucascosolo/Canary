"""The World Bank Indicators API, for four series."""

from __future__ import annotations

import datetime
import re
from collections.abc import Sequence
from typing import Any

from canary.adapters.base import (
    Adapter,
    Misses,
    ParseResult,
    ReleaseRef,
    by_name,
    column_digest,
    load_json,
    number,
    read_bytes,
    whole_year,
    year_period,
)
from canary.errors import SchemaChanged
from canary.observations import IndicatorSpec, ObservationRow
from canary.rawstore import RawRef, RawStore

BASE = "https://api.worldbank.org/v2"
COUNTRY_URL = f"{BASE}/country?format=json&per_page=400"
FIELDS = ("countryiso3code", "date", "value")
SERIES = (
    ("FP.CPI.TOTL.ZG", "Inflation, consumer prices", "annual %", "up"),
    ("NY.GDP.PCAP.KD.ZG", "GDP per capita growth", "annual %", "down"),
    ("SL.UEM.TOTL.ZS", "Unemployment, total", "% of total labor force", "up"),
    ("SP.POP.TOTL", "Population, total", "people", "none"),
)
BIAS = (
    "Compiled from national statistical offices, so definitions and quality differ between "
    "countries, and recent years are often estimates that are revised later."
)


def _series_url(code: str) -> str:
    year = datetime.datetime.now(datetime.UTC).year
    return f"{BASE}/country/all/indicator/{code}?format=json&per_page=20000&date=1960:{year}"


def _body(data: bytes, what: str) -> tuple[dict[str, Any], list[dict[str, Any]]]:
    """The API's two-element answer; it reports errors as a one-element list with HTTP 200."""
    body = load_json(data, what)
    if not isinstance(body, list) or len(body) != 2 or not isinstance(body[0], dict):
        raise SchemaChanged(f"{what}: expected a header and a list, got {str(body)[:200]}")
    return body[0], body[1] or []


class WorldBank(Adapter):
    source_id = "world-bank-indicators"

    def config(self) -> Any:
        return {"series": SERIES}

    def discover(self, fetcher: Any) -> ReleaseRef:
        first = _series_url(SERIES[0][0])
        header, _ = _body(self._remember(fetcher, first), SERIES[0][0])
        if not header.get("lastupdated"):
            raise SchemaChanged("missing column lastupdated in the World Bank response")
        urls = {"country.json": COUNTRY_URL}
        urls.update({f"{code}.json": _series_url(code) for code, *_ in SERIES})
        return ReleaseRef(str(header["lastupdated"]), urls)

    def _pages(self, fetcher: Any, store: RawStore, stem: str, url: str) -> list[RawRef]:
        data = self._take(fetcher, url)
        pages = int(_body(data, stem)[0].get("pages") or 1)
        refs = [store.put(self.source_id, f"{stem}.page1.json", data)]
        for page in range(2, pages + 1):
            data = fetcher.get(f"{url}&page={page}")
            refs.append(store.put(self.source_id, f"{stem}.page{page}.json", data))
        return refs

    def fetch(self, fetcher: Any, ref: ReleaseRef, store: RawStore) -> list[RawRef]:
        refs = []
        for name, url in ref.urls.items():
            refs += self._pages(fetcher, store, name.removesuffix(".json"), url)
        return refs

    def parse(self, refs: Sequence[RawRef], resolver: Any) -> ParseResult:
        files = by_name(refs)
        aggregates = _aggregates(_entries(files, "country"))
        rows = []
        misses = Misses()
        for code, *_ in SERIES:
            entries = _entries(files, code)
            for entry in entries:
                for key in FIELDS:
                    if key not in entry:
                        raise SchemaChanged(f"missing column {key} in {code}")
                geo = (entry["countryiso3code"] or "").strip()
                if not geo:
                    misses.add((entry.get("country") or {}).get("value"))
                    continue
                if geo in aggregates:
                    misses.skipped += 1
                    continue
                if entry["value"] is None:
                    continue
                start, end = year_period(whole_year(entry["date"], "date"))
                value = number(entry["value"], "value")
                rows.append(ObservationRow(f"wb-{code}", geo, start, end, value))
        return ParseResult(
            indicators=[
                IndicatorSpec(
                    id=f"wb-{code}",
                    source_id=self.source_id,
                    name=name,
                    definition=f"{name}, World Bank series {code}.",
                    domain="economy",
                    unit=unit,
                    cadence="annual",
                    deterioration_direction=direction,
                    reporting_bias_note=BIAS,
                )
                for code, name, unit, direction in SERIES
            ],
            rows=rows,
            skipped=misses.skipped,
            unmapped=misses.unmapped,
            schema_digest=column_digest(FIELDS + ("region",)),
        )


def _entries(files: dict[str, RawRef], stem: str) -> list[dict[str, Any]]:
    pattern = re.compile(re.escape(stem) + r"\.page(\d+)\.json")
    found = sorted(
        (int(match.group(1)), name)
        for name in files
        if (match := pattern.fullmatch(name)) is not None
    )
    if not found:
        raise SchemaChanged(f"no World Bank file for {stem}")
    entries: list[dict[str, Any]] = []
    for _, name in found:
        entries += _body(read_bytes(files[name]), stem)[1]
    return entries


def _aggregates(countries: list[dict[str, Any]]) -> set[str]:
    aggregates = set()
    for country in countries:
        try:
            if country["region"]["value"].strip() == "Aggregates":
                aggregates.add(country["id"])
        except (KeyError, TypeError, AttributeError) as exc:
            raise SchemaChanged(f"missing column region in the country list: {exc}") from exc
    return aggregates
