"""The Early Warning Project's Statistical Risk Assessment, shown unchanged."""

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
    column_digest,
    csv_header,
    csv_rows,
    is_blank,
    number,
    only_ref,
    read_bytes,
)
from canary.errors import FetchFailed, SchemaChanged
from canary.observations import IndicatorSpec, ObservationRow
from canary.rawstore import RawRef

DOWNLOAD = "https://earlywarningproject.ushmm.org/api/sra/download/csv/{year}-sra"
YEARS_TRIED = 4
RISK_COLUMN = re.compile(r"risk_in_(\d{4})_(\d{2}|\d{4})")
BIAS = (
    "A statistical model's estimate of rare events, built on data that are themselves incomplete, "
    "so it is not a prediction for any one country."
)


def _risk_period(header: list[str]) -> tuple[str, datetime.date, datetime.date]:
    matches = [(c, m) for c in header if (m := RISK_COLUMN.fullmatch(c)) is not None]
    if len(matches) != 1:
        raise SchemaChanged(f"missing column risk_in_<y1>_<y2>: found {[c for c, _ in matches]}")
    column, match = matches[0]
    first, second = int(match.group(1)), match.group(2)
    last = first // 100 * 100 + int(second) if len(second) == 2 else int(second)
    if last < first:
        raise SchemaChanged(f"column {column} ends before it starts")
    return column, datetime.date(first, 1, 1), datetime.date(last, 12, 31)


def _spec(indicator_id: str, name: str, unit: str, direction: str) -> IndicatorSpec:
    return IndicatorSpec(
        id=indicator_id,
        source_id="ewp-sra",
        name=name,
        definition=f"{name}, as published by the Early Warning Project.",
        domain="conflict",
        unit=unit,
        cadence="annual",
        deterioration_direction=direction,
        reporting_bias_note=BIAS,
    )


class EwpSra(Adapter):
    source_id = "ewp-sra"

    def config(self) -> Any:
        return {"download": DOWNLOAD, "years_tried": YEARS_TRIED, "risk": RISK_COLUMN.pattern}

    def discover(self, fetcher: Any) -> ReleaseRef:
        this_year = datetime.date.today().year
        for year in range(this_year + 1, this_year + 1 - YEARS_TRIED, -1):
            label = f"{year}-sra"
            url = DOWNLOAD.format(year=year)
            try:
                self._remember(fetcher, url)
            except FetchFailed:
                continue
            return ReleaseRef(label, {label: url})
        raise FetchFailed(f"no SRA file for the {YEARS_TRIED} years up to {this_year + 1}")

    def parse(self, refs: Sequence[RawRef], resolver: Any) -> ParseResult:
        data = read_bytes(only_ref(refs))
        risk, start, end = _risk_period(csv_header(data))
        required = ["ISO3", "riskrank", risk]
        rows = []
        misses = Misses()
        for record in csv_rows(data, required):
            code = record["ISO3"]
            if is_blank(code):
                misses.add(record.get("country"))
                continue
            for indicator_id, column in (("ewp-sra-risk", risk), ("ewp-sra-rank", "riskrank")):
                if not is_blank(record[column]):
                    value = number(record[column], column)
                    rows.append(ObservationRow(indicator_id, code, start, end, value))
        return ParseResult(
            indicators=[
                _spec("ewp-sra-risk", "Risk of a new mass killing", "probability", "up"),
                _spec("ewp-sra-rank", "Rank by risk of a new mass killing", "rank", "none"),
            ],
            rows=rows,
            skipped=misses.skipped,
            unmapped=misses.unmapped,
            schema_digest=column_digest(required),
        )
