"""Cline Center coups. Downloaded by hand: its data bank refuses scripts, so this never fetches."""

from __future__ import annotations

import os
import pathlib
import re
from collections import defaultdict
from collections.abc import Sequence
from typing import Any

from canary.adapters.base import (
    Adapter,
    Misses,
    ParseResult,
    ReleaseRef,
    column_digest,
    csv_rows,
    is_blank,
    number,
    only_ref,
    read_bytes,
    whole_year,
    year_period,
)
from canary.errors import ManualFileMissing
from canary.observations import IndicatorSpec, ObservationRow
from canary.rawstore import RawRef, RawStore

PAGE = "https://databank.illinois.edu/datasets/IDB-7095878"
FLAGS = (
    ("cline-realized", "realized", "Coups realized"),
    ("cline-attempts", "attempt", "Coup attempts"),
    ("cline-conspiracies", "conspiracy", "Coup conspiracies"),
)
REQUIRED = ("country", "year", "realized", "attempt", "conspiracy")
VERSION = re.compile(r"\d+(?:\.\d+)+")
BIAS = (
    "Built from news and scholarly records, so conspiracies that never surfaced publicly are "
    "missing, and older or less-covered cases are likelier to be."
)


def drop_folder(source_id: str) -> pathlib.Path:
    configured = os.environ.get("CANARY_DROP_DIR")
    root = pathlib.Path(configured) if configured else pathlib.Path.home() / ".cache/canary/drop"
    return root / source_id


class ClineCoups(Adapter):
    source_id = "cline-coups"
    needs_resolver = True

    def config(self) -> Any:
        return {"columns": REQUIRED, "page": PAGE}

    def discover(self, fetcher: Any) -> ReleaseRef:
        folder = drop_folder(self.source_id)
        files = sorted(folder.glob("*.csv"))
        if len(files) != 1:
            raise ManualFileMissing(
                f"expected one CSV in {folder}, found {len(files)}: download it from {PAGE}"
            )
        found = VERSION.search(files[0].name)
        label = found.group(0) if found else "unknown"
        return ReleaseRef(label, {files[0].name: str(files[0])})

    def fetch(self, fetcher: Any, ref: ReleaseRef, store: RawStore) -> list[RawRef]:
        return [
            store.put(self.source_id, name, pathlib.Path(path).read_bytes())
            for name, path in ref.urls.items()
        ]

    def parse(self, refs: Sequence[RawRef], resolver: Any) -> ParseResult:
        totals: dict[tuple[str, int], list[float]] = defaultdict(lambda: [0.0, 0.0, 0.0])
        misses = Misses()
        for record in csv_rows(read_bytes(only_ref(refs)), REQUIRED):
            code = resolver.resolve(record["country"] or "")
            if code is None:
                misses.add(record["country"])
                continue
            total = totals[(code, whole_year(record["year"], "year"))]
            for position, (_, column, _) in enumerate(FLAGS):
                if not is_blank(record[column]):
                    total[position] += number(record[column], column)

        rows = []
        for (code, year), values in sorted(totals.items()):
            start, end = year_period(year)
            for (indicator_id, _, _), value in zip(FLAGS, values, strict=True):
                rows.append(ObservationRow(indicator_id, code, start, end, value))
        return ParseResult(
            indicators=[
                IndicatorSpec(
                    id=indicator_id,
                    source_id=self.source_id,
                    name=name,
                    definition=f"{name} per country and year, the sum of the {column} flag.",
                    domain="institutions",
                    unit="events",
                    cadence="annual",
                    deterioration_direction="up",
                    reporting_bias_note=BIAS,
                )
                for indicator_id, column, name in FLAGS
            ],
            rows=rows,
            skipped=misses.skipped,
            unmapped=misses.unmapped,
            schema_digest=column_digest(REQUIRED),
        )
