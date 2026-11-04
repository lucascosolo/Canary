"""V-Dem: the Country-Year dataset from its R package, and Episodes of Regime Transformation."""

from __future__ import annotations

from collections.abc import Iterable, Mapping, Sequence
from typing import Any

from canary.adapters.base import (
    Adapter,
    Misses,
    ParseResult,
    ReleaseRef,
    by_name,
    column_digest,
    csv_rows,
    description_version,
    is_blank,
    number,
    only_ref,
    optional_number,
    read_bytes,
    whole_year,
    year_period,
)
from canary.errors import SchemaChanged
from canary.observations import IndicatorSpec, ObservationRow
from canary.rawstore import RawRef

VDEM_BASE = "https://raw.githubusercontent.com/vdeminstitute/vdemdata/master/"
ERT_BASE = "https://raw.githubusercontent.com/vdeminstitute/ERT/master/"
COLUMNS = (
    "v2x_polyarchy",
    "v2x_libdem",
    "v2x_partipdem",
    "v2x_delibdem",
    "v2x_egaldem",
    "v2x_jucon",
    "v2xlg_legcon",
    "v2x_freexp_altinf",
    "v2x_frassoc_thick",
    "v2xcl_rol",
    "v2x_cspart",
    "v2x_civlib",
    "v2x_clphy",
    "v2xel_frefair",
    "v2x_corr",
)
REQUIRED = ["country_text_id", "year"]
for _column in COLUMNS:
    REQUIRED += [_column, f"{_column}_codelow", f"{_column}_codehigh"]
UP_IS_WORSE = ("v2x_corr",)
VDEM_BIAS = (
    "Expert-coded, so scores carry the judgement of the coders, and past years can change "
    "between releases."
)


def rows_from_records(
    records: Iterable[Mapping[str, Any]], codebook: Mapping[str, Mapping[str, str]]
) -> ParseResult:
    """Turn V-Dem records, as plain dicts, into indicators and rows."""
    indicators = []
    for column in COLUMNS:
        if column not in codebook:
            raise SchemaChanged(f"missing column {column} in the V-Dem codebook")
        indicators.append(
            IndicatorSpec(
                id=f"vdem-{column}",
                source_id="vdem-country-year",
                name=codebook[column]["name"],
                definition=codebook[column]["definition"],
                domain="institutions",
                unit="index",
                cadence="annual",
                deterioration_direction="up" if column in UP_IS_WORSE else "down",
                reporting_bias_note=VDEM_BIAS,
            )
        )
    rows = []
    misses = Misses()
    for record in records:
        for column in REQUIRED:
            if column not in record:
                raise SchemaChanged(f"missing column {column}")
        code = record["country_text_id"]
        if is_blank(code):
            misses.add(record.get("country_name"))
            continue
        start, end = year_period(whole_year(record["year"], "year"))
        for column in COLUMNS:
            if is_blank(record[column]):
                continue
            rows.append(
                ObservationRow(
                    f"vdem-{column}",
                    str(code),
                    start,
                    end,
                    number(record[column], column),
                    optional_number(record[f"{column}_codelow"], f"{column}_codelow"),
                    optional_number(record[f"{column}_codehigh"], f"{column}_codehigh"),
                )
            )
    return ParseResult(
        indicators=indicators,
        rows=rows,
        skipped=misses.skipped,
        unmapped=misses.unmapped,
        schema_digest=column_digest(REQUIRED),
    )


def _read_codebook(frame: Any) -> dict[str, dict[str, str]]:
    columns = set(frame.columns)
    for column in ("tag", "name"):
        if column not in columns:
            raise SchemaChanged(f"missing column {column} in the V-Dem codebook")
    meaning = next((c for c in ("definition", "clarification", "question") if c in columns), None)
    if meaning is None:
        raise SchemaChanged("missing column definition in the V-Dem codebook")
    return {
        record["tag"]: {
            "name": record["name"],
            "definition": record["name"] if is_blank(record[meaning]) else record[meaning],
        }
        for record in frame[["tag", "name", meaning]].to_dict("records")
        if record["tag"] in COLUMNS
    }


class VdemCountryYear(Adapter):
    source_id = "vdem-country-year"

    def config(self) -> Any:
        return {"columns": COLUMNS, "up": UP_IS_WORSE}

    def discover(self, fetcher: Any) -> ReleaseRef:
        label = description_version(fetcher.get(VDEM_BASE + "DESCRIPTION"))
        urls = {
            "vdem.RData": VDEM_BASE + "data/vdem.RData",
            "codebook.RData": VDEM_BASE + "data/codebook.RData",
        }
        return ReleaseRef(label, urls)

    def parse(self, refs: Sequence[RawRef], resolver: Any) -> ParseResult:
        import pyreadr
        from pyreadr.custom_errors import LibrdataError, PyreadrError

        files = by_name(refs)
        try:
            data = pyreadr.read_r(files["vdem.RData"].path)
            codebook = pyreadr.read_r(files["codebook.RData"].path)
        except (KeyError, LibrdataError, PyreadrError) as exc:
            raise SchemaChanged(f"unreadable V-Dem file: {exc}") from exc
        if "vdem" not in data or "codebook" not in codebook:
            raise SchemaChanged("missing object vdem or codebook in the V-Dem R files")
        frame = data["vdem"]
        for column in REQUIRED:
            if column not in frame.columns:
                raise SchemaChanged(f"missing column {column}")
        return rows_from_records(
            frame[REQUIRED].to_dict("records"), _read_codebook(codebook["codebook"])
        )


ERT_SERIES = (
    (
        "ert-aut-ep",
        "aut_ep",
        "Autocratization episode",
        "Whether the country-year falls in an episode of autocratization.",
        "up",
    ),
    (
        "ert-dem-ep",
        "dem_ep",
        "Democratization episode",
        "Whether the country-year falls in an episode of democratization.",
        "none",
    ),
)


class VdemErt(Adapter):
    source_id = "vdem-ert"

    def config(self) -> Any:
        return {"series": ERT_SERIES}

    def discover(self, fetcher: Any) -> ReleaseRef:
        label = description_version(fetcher.get(ERT_BASE + "DESCRIPTION"))
        return ReleaseRef(label, {"ert.csv": ERT_BASE + "inst/ert.csv"})

    def parse(self, refs: Sequence[RawRef], resolver: Any) -> ParseResult:
        required = ["country_text_id", "year"] + [series[1] for series in ERT_SERIES]
        rows = []
        misses = Misses()
        for record in csv_rows(read_bytes(only_ref(refs)), required):
            code = record["country_text_id"]
            if is_blank(code):
                misses.add(record.get("country_name"))
                continue
            start, end = year_period(whole_year(record["year"], "year"))
            for indicator_id, column, *_ in ERT_SERIES:
                if not is_blank(record[column]):
                    rows.append(
                        ObservationRow(
                            indicator_id, code, start, end, number(record[column], column)
                        )
                    )
        indicators = [
            IndicatorSpec(
                id=indicator_id,
                source_id=self.source_id,
                name=name,
                definition=definition,
                domain="institutions",
                unit="0 or 1",
                cadence="annual",
                deterioration_direction=direction,
                reporting_bias_note=(
                    "Derived by rule from V-Dem's expert-coded scores, so it inherits their "
                    "judgement and can change between releases."
                ),
            )
            for indicator_id, _, name, definition, direction in ERT_SERIES
        ]
        return ParseResult(
            indicators=indicators,
            rows=rows,
            skipped=misses.skipped,
            unmapped=misses.unmapped,
            schema_digest=column_digest(required),
        )
