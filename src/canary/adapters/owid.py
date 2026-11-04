"""Our World in Data: only the series on a cleared allow-list. Upstream terms vary by series."""

from __future__ import annotations

from collections.abc import Sequence
from typing import Any

from canary.adapters.base import (
    Adapter,
    Misses,
    ParseResult,
    ReleaseRef,
    by_name,
    column_digest,
    csv_rows,
    is_blank,
    load_json,
    number,
    read_bytes,
    whole_year,
    year_period,
)
from canary.errors import SchemaChanged
from canary.observations import IndicatorSpec, ObservationRow
from canary.rawstore import RawRef

BASE = "https://ourworldindata.org/grapher/"
SERIES: list[str] = []
BIAS = "A compilation of other providers' data, so coverage and method follow each upstream source."


def _columns(metadata: Any, slug: str) -> dict[str, dict[str, Any]]:
    if not isinstance(metadata, dict) or not isinstance(metadata.get("columns"), dict):
        raise SchemaChanged(f"missing column columns in the metadata of {slug}")
    return metadata["columns"]


class OurWorldInData(Adapter):
    source_id = "our-world-in-data"

    def __init__(self, series: Sequence[str]) -> None:
        super().__init__()
        self.series = list(series)

    def config(self) -> Any:
        return {"series": sorted(self.series)}

    def discover(self, fetcher: Any) -> ReleaseRef:
        urls: dict[str, str] = {}
        updated: list[str] = []
        for slug in self.series:
            metadata_url = f"{BASE}{slug}.metadata.json"
            metadata = load_json(self._remember(fetcher, metadata_url), slug)
            for column in _columns(metadata, slug).values():
                if column.get("lastUpdated"):
                    updated.append(str(column["lastUpdated"]))
            urls[f"{slug}.csv"] = f"{BASE}{slug}.csv?useColumnShortNames=true"
            urls[f"{slug}.metadata.json"] = metadata_url
        return ReleaseRef(max(updated, default="none"), urls)

    def parse(self, refs: Sequence[RawRef], resolver: Any) -> ParseResult:
        files = by_name(refs)
        indicators = []
        rows = []
        misses = Misses()
        read_columns = {"entity", "code", "year"}
        for slug in self.series:
            columns = _columns(load_json(read_bytes(files[f"{slug}.metadata.json"]), slug), slug)
            read_columns |= set(columns)
            required = ["entity", "code", "year", *columns]
            for record in csv_rows(read_bytes(files[f"{slug}.csv"]), required):
                code = record["code"]
                if is_blank(code):
                    misses.add(record["entity"])
                    continue
                start, end = year_period(whole_year(record["year"], "year"))
                for column in columns:
                    if not is_blank(record[column]):
                        indicator = f"owid-{slug}-{column}"
                        value = number(record[column], column)
                        rows.append(ObservationRow(indicator, code, start, end, value))
            for column, details in columns.items():
                if not details.get("titleShort"):
                    raise SchemaChanged(f"missing column titleShort in the metadata of {column}")
                indicators.append(
                    IndicatorSpec(
                        id=f"owid-{slug}-{column}",
                        source_id=self.source_id,
                        name=details["titleShort"],
                        definition=details.get("descriptionShort") or details["titleShort"],
                        domain="economy",
                        unit=details.get("unit") or "",
                        cadence="annual",
                        deterioration_direction="none",
                        reporting_bias_note=BIAS,
                    )
                )
        return ParseResult(
            indicators=indicators,
            rows=rows,
            skipped=misses.skipped,
            unmapped=misses.unmapped,
            schema_digest=column_digest(read_columns),
        )
