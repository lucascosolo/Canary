"""Reference loads: GeoNames countries, Wikidata identifiers and the Natural Earth map file."""

from __future__ import annotations

import hashlib
import re
import urllib.parse
from collections.abc import Sequence
from typing import Any

from canary.adapters.base import (
    Adapter,
    Misses,
    ParseResult,
    PlaceRow,
    ReleaseRef,
    column_digest,
    csv_rows,
    decode,
    number,
    only_ref,
    read_bytes,
)
from canary.errors import SchemaChanged
from canary.rawstore import RawRef

GEONAMES_URL = "https://download.geonames.org/export/dump/countryInfo.txt"
GEONAMES_COLUMNS = ("ISO", "ISO3", "Country", "Continent", "geonameid")
WIKIDATA_QUERY = "SELECT ?item ?code WHERE { ?item wdt:P298 ?code . }"
WIKIDATA_URL = "https://query.wikidata.org/sparql?" + urllib.parse.urlencode(
    {"query": WIKIDATA_QUERY}
)
WIKIDATA_COLUMNS = ("item", "code")
Q_ID = re.compile(r"/entity/(Q(\d+))$")
NATURAL_EARTH_URL = (
    "https://naciscdn.org/naturalearth/50m/cultural/ne_50m_admin_0_countries.zip"
)


def _label(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()[:12]


class GeoNames(Adapter):
    source_id = "geonames"

    def config(self) -> Any:
        return {"url": GEONAMES_URL, "columns": GEONAMES_COLUMNS}

    def discover(self, fetcher: Any) -> ReleaseRef:
        data = self._remember(fetcher, GEONAMES_URL)
        return ReleaseRef(_label(data), {"countryInfo.txt": GEONAMES_URL})

    def parse(self, refs: Sequence[RawRef], resolver: Any) -> ParseResult:
        lines = decode(read_bytes(only_ref(refs)), "countryInfo.txt").split("\n")
        header = next((line for line in lines if line.startswith("#ISO\t")), None)
        if header is None:
            raise SchemaChanged("missing column ISO: no #ISO header line in countryInfo.txt")
        names = header.lstrip("#").rstrip("\r").split("\t")
        for column in GEONAMES_COLUMNS:
            if column not in names:
                raise SchemaChanged(f"missing column {column} in countryInfo.txt")
        position = {column: names.index(column) for column in GEONAMES_COLUMNS}

        places = []
        misses = Misses()
        for line in lines:
            line = line.rstrip("\r")
            if not line.strip() or line.startswith("#"):
                continue
            cells = line.split("\t")
            if len(cells) <= max(position.values()):
                raise SchemaChanged(f"short line in countryInfo.txt: {line[:80]!r}")
            iso3 = cells[position["ISO3"]].strip()
            if not iso3:
                misses.add(cells[position["Country"]])
                continue
            places.append(
                PlaceRow(
                    id=iso3,
                    iso2=cells[position["ISO"]].strip(),
                    name=cells[position["Country"]].strip(),
                    continent=cells[position["Continent"]].strip(),
                    geonames_id=int(number(cells[position["geonameid"]], "geonameid")),
                )
            )
        return ParseResult(
            places=places,
            skipped=misses.skipped,
            unmapped=misses.unmapped,
            schema_digest=column_digest(GEONAMES_COLUMNS),
        )


class Wikidata(Adapter):
    source_id = "wikidata"

    def config(self) -> Any:
        return {"query": WIKIDATA_QUERY}

    def discover(self, fetcher: Any) -> ReleaseRef:
        data = self._remember(fetcher, WIKIDATA_URL, headers={"Accept": "text/csv"})
        return ReleaseRef(_label(data), {"iso3.csv": WIKIDATA_URL})

    def parse(self, refs: Sequence[RawRef], resolver: Any) -> ParseResult:
        smallest: dict[str, tuple[int, str]] = {}
        skipped = 0
        for record in csv_rows(read_bytes(only_ref(refs)), WIKIDATA_COLUMNS):
            found = Q_ID.search(record["item"] or "")
            code = (record["code"] or "").strip()
            if found is None or not code:
                skipped += 1
                continue
            candidate = (int(found.group(2)), found.group(1))
            if code not in smallest or candidate < smallest[code]:
                smallest[code] = candidate
        return ParseResult(
            wikidata_ids={code: item for code, (_, item) in smallest.items()},
            skipped=skipped,
            schema_digest=column_digest(WIKIDATA_COLUMNS),
        )


class NaturalEarth(Adapter):
    source_id = "natural-earth"

    def config(self) -> Any:
        return {"url": NATURAL_EARTH_URL}

    def discover(self, fetcher: Any) -> ReleaseRef:
        data = self._remember(fetcher, NATURAL_EARTH_URL)
        return ReleaseRef(_label(data), {"ne_50m_admin_0_countries.zip": NATURAL_EARTH_URL})

    def parse(self, refs: Sequence[RawRef], resolver: Any) -> ParseResult:
        return ParseResult(schema_digest=column_digest([]))
