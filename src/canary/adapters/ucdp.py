"""UCDP: the candidate events, the annual GED and the UCDP/PRIO Armed Conflict Dataset."""

from __future__ import annotations

import re
from collections import defaultdict
from collections.abc import Iterable, Sequence
from typing import Any

from canary.adapters.base import (
    Adapter,
    Misses,
    ParseResult,
    ReleaseRef,
    basename,
    column_digest,
    csv_rows,
    highest_link,
    is_blank,
    month_period,
    number,
    only_csv_in_zip,
    only_ref,
    page_link,
    read_bytes,
    whole_year,
    year_period,
)
from canary.errors import SchemaChanged
from canary.observations import IndicatorSpec, ObservationRow
from canary.rawstore import RawRef

DOWNLOADS = "https://ucdp.uu.se/downloads/"
CANDIDATE_MONTHLY = re.compile(r"/GEDEvent_v(\d+)_01_(\d+)_(\d+)\.csv$")
CANDIDATE_ZERO = re.compile(r"/GEDEvent_v(\d+)_0_(\d+)\.csv$")
GED_ZIP = re.compile(r"/ged(\d+)-csv\.zip$")
ACD_ZIP = re.compile(r"/ucdp-prio-acd-(\d+)-csv\.zip$")
EVENT_COLUMNS = ("country", "date_start", "best", "low", "high")
ACD_COLUMNS = ("location", "year", "intensity_level")
MONTH = re.compile(r"(\d{4})-(\d{2})")
CANDIDATE_BIAS = (
    "Preliminary: events are coded quickly from media reports and often carry 'Check' code "
    "statuses, so counts can change when UCDP finishes its review."
)
GED_BIAS = (
    "Coded from media and other reports, so places with less reporting can appear calmer than "
    "they are."
)
ACD_BIAS = (
    "Counts conflicts past UCDP's battle-death threshold where a state is a party, as far as "
    "reporting shows them, so smaller or unreported violence does not appear."
)


def _sum(value: Any, column: str) -> float:
    return 0.0 if is_blank(value) else number(value, column)


def parse_events(
    data: bytes, prefix: str, source_id: str, cadence: str, bias: str, resolver: Any
) -> ParseResult:
    totals: dict[tuple[str, int, int], list[float]] = defaultdict(lambda: [0.0, 0.0, 0.0, 0.0])
    misses = Misses()
    for record in csv_rows(data, EVENT_COLUMNS):
        code = resolver.resolve(record["country"] or "")
        if code is None:
            misses.add(record["country"])
            continue
        month = MONTH.match(record["date_start"] or "")
        if month is None:
            raise SchemaChanged(f"column date_start holds a non-date: {record['date_start']!r}")
        total = totals[(code, int(month.group(1)), int(month.group(2)))]
        total[0] += 1
        total[1] += _sum(record["best"], "best")
        total[2] += _sum(record["low"], "low")
        total[3] += _sum(record["high"], "high")

    rows = []
    for (code, year, month_number), (events, best, low, high) in sorted(totals.items()):
        start, end = month_period(year, month_number)
        rows.append(ObservationRow(f"{prefix}-events", code, start, end, events))
        rows.append(ObservationRow(f"{prefix}-deaths", code, start, end, best, low, high))
    return ParseResult(
        indicators=[
            _spec(f"{prefix}-events", source_id, "Violent events", "events", cadence, bias),
            _spec(f"{prefix}-deaths", source_id, "Deaths in events", "deaths", cadence, bias),
        ],
        rows=rows,
        skipped=misses.skipped,
        unmapped=misses.unmapped,
        schema_digest=column_digest(EVENT_COLUMNS),
    )


def _spec(
    indicator_id: str, source_id: str, name: str, unit: str, cadence: str, bias: str
) -> IndicatorSpec:
    return IndicatorSpec(
        id=indicator_id,
        source_id=source_id,
        name=name,
        definition=f"{name}, per country and period, as coded by UCDP.",
        domain="conflict",
        unit=unit,
        cadence=cadence,
        deterioration_direction="up",
        reporting_bias_note=bias,
    )


def _candidate_release(page: bytes) -> ReleaseRef:
    found = page_link(page, DOWNLOADS, CANDIDATE_MONTHLY) or highest_link(
        page, DOWNLOADS, CANDIDATE_ZERO
    )
    url, _ = found
    name = basename(url)
    return ReleaseRef(name.removeprefix("GEDEvent_v").removesuffix(".csv"), {name: url})


class UcdpCandidate(Adapter):
    source_id = "ucdp-candidate"
    needs_resolver = True

    def config(self) -> Any:
        return {"columns": EVENT_COLUMNS}

    def discover(self, fetcher: Any) -> ReleaseRef:
        return _candidate_release(fetcher.get(DOWNLOADS))

    def parse(self, refs: Sequence[RawRef], resolver: Any) -> ParseResult:
        data = read_bytes(only_ref(refs))
        return parse_events(
            data, "ucdp-candidate", self.source_id, "monthly", CANDIDATE_BIAS, resolver
        )


class UcdpGed(Adapter):
    source_id = "ucdp-ged"
    needs_resolver = True

    def config(self) -> Any:
        return {"columns": EVENT_COLUMNS}

    def discover(self, fetcher: Any) -> ReleaseRef:
        url, match = highest_link(fetcher.get(DOWNLOADS), DOWNLOADS, GED_ZIP)
        return ReleaseRef(match.group(1), {basename(url): url})

    def parse(self, refs: Sequence[RawRef], resolver: Any) -> ParseResult:
        data = only_csv_in_zip(read_bytes(only_ref(refs)))
        return parse_events(data, "ucdp-ged", self.source_id, "annual", GED_BIAS, resolver)


def _split_location(location: str | None) -> Iterable[str]:
    return [part for part in (location or "").split(", ") if part.strip()]


class UcdpPrioAcd(Adapter):
    source_id = "ucdp-prio-acd"
    needs_resolver = True

    def config(self) -> Any:
        return {"columns": ACD_COLUMNS}

    def discover(self, fetcher: Any) -> ReleaseRef:
        url, match = highest_link(fetcher.get(DOWNLOADS), DOWNLOADS, ACD_ZIP)
        return ReleaseRef(match.group(1), {basename(url): url})

    def parse(self, refs: Sequence[RawRef], resolver: Any) -> ParseResult:
        counts: dict[tuple[str, int], list[int]] = defaultdict(lambda: [0, 0])
        misses = Misses()
        data = only_csv_in_zip(read_bytes(only_ref(refs)))
        for record in csv_rows(data, ACD_COLUMNS):
            year = whole_year(record["year"], "year")
            war = number(record["intensity_level"], "intensity_level") == 2
            resolved = False
            for name in _split_location(record["location"]):
                code = resolver.resolve(name)
                if code is None:
                    misses.note(name)
                    continue
                resolved = True
                counts[(code, year)][0] += 1
                counts[(code, year)][1] += int(war)
            if not resolved:
                misses.skipped += 1

        rows: list[ObservationRow] = []
        for (code, year), (active, wars) in sorted(counts.items()):
            start, end = year_period(year)
            rows.append(ObservationRow("acd-active-conflicts", code, start, end, float(active)))
            rows.append(ObservationRow("acd-war-conflicts", code, start, end, float(wars)))
        return ParseResult(
            indicators=[
                _spec(
                    "acd-active-conflicts",
                    self.source_id,
                    "Active armed conflicts",
                    "conflicts",
                    "annual",
                    ACD_BIAS,
                ),
                _spec(
                    "acd-war-conflicts",
                    self.source_id,
                    "Armed conflicts at war intensity",
                    "conflicts",
                    "annual",
                    ACD_BIAS,
                ),
            ],
            rows=rows,
            skipped=misses.skipped,
            unmapped=misses.unmapped,
            schema_digest=column_digest(ACD_COLUMNS),
        )
