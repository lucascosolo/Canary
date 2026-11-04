"""What every adapter shares: the interface, the result types and the parsing helpers."""

from __future__ import annotations

import calendar
import csv
import datetime
import hashlib
import io
import json
import math
import pathlib
import re
import sys
import urllib.parse
import zipfile
from collections.abc import Iterable, Iterator, Sequence
from dataclasses import dataclass, field
from typing import Any

from canary.errors import SchemaChanged
from canary.geo import CountryResolver
from canary.http import Fetcher
from canary.observations import IndicatorSpec, ObservationRow
from canary.rawstore import RawRef, RawStore

csv.field_size_limit(sys.maxsize)
MAX_ZIP_MEMBER_BYTES = 2_000_000_000


@dataclass(frozen=True)
class ReleaseRef:
    version_label: str
    urls: dict[str, str]
    released_at: datetime.datetime | None = None


@dataclass(frozen=True)
class PlaceRow:
    id: str
    iso2: str
    name: str
    continent: str
    geonames_id: int


@dataclass(frozen=True)
class ParseResult:
    indicators: list[IndicatorSpec] = field(default_factory=list)
    rows: list[ObservationRow] = field(default_factory=list)
    places: list[PlaceRow] = field(default_factory=list)
    skipped: int = 0
    unmapped: list[str] = field(default_factory=list)
    schema_digest: str = ""
    wikidata_ids: dict[str, str] = field(default_factory=dict)

    @property
    def parsed_count(self) -> int:
        return len(self.rows) + len(self.places) + len(self.wikidata_ids)


class Adapter:
    source_id = ""
    needs_resolver = False

    def __init__(self) -> None:
        self._bodies: dict[str, bytes] = {}

    def config(self) -> Any:
        return None

    def config_digest(self) -> str:
        text = json.dumps([self.source_id, self.config()], sort_keys=True)
        return hashlib.sha256(text.encode("utf-8")).hexdigest()

    def _remember(self, fetcher: Fetcher, url: str, **kwargs: Any) -> bytes:
        """Fetch a file discover has to read, so fetch can store it without a second request."""
        self._bodies[url] = fetcher.get(url, **kwargs)
        return self._bodies[url]

    def _take(self, fetcher: Fetcher, url: str) -> bytes:
        return self._bodies.pop(url) if url in self._bodies else fetcher.get(url)

    def discover(self, fetcher: Fetcher) -> ReleaseRef:
        raise NotImplementedError

    def fetch(self, fetcher: Fetcher, ref: ReleaseRef, store: RawStore) -> list[RawRef]:
        return [
            store.put(self.source_id, name, self._take(fetcher, url))
            for name, url in ref.urls.items()
        ]

    def parse(self, refs: Sequence[RawRef], resolver: CountryResolver | None) -> ParseResult:
        raise NotImplementedError


class Misses:
    """Rows left out for having no country, and the source names behind them."""

    def __init__(self) -> None:
        self.skipped = 0
        self.names: set[str] = set()

    def add(self, name: Any) -> None:
        self.skipped += 1
        self.note(name)

    def note(self, name: Any) -> None:
        if not is_blank(name):
            self.names.add(str(name).strip())

    @property
    def unmapped(self) -> list[str]:
        return sorted(self.names)


def is_blank(value: Any) -> bool:
    if value is None:
        return True
    if isinstance(value, float):
        return math.isnan(value)
    return isinstance(value, str) and value.strip() in ("", "NA", "NaN")


def number(value: Any, column: str) -> float:
    try:
        return float(value)
    except (TypeError, ValueError) as exc:
        raise SchemaChanged(f"column {column} holds a non-number: {value!r}") from exc


def optional_number(value: Any, column: str) -> float | None:
    return None if is_blank(value) else number(value, column)


def whole_year(value: Any, column: str) -> int:
    year = number(value, column)
    if not year.is_integer() or not 1 <= year <= 9999:
        raise SchemaChanged(f"column {column} holds a non-year: {value!r}")
    return int(year)


def year_period(year: int) -> tuple[datetime.date, datetime.date]:
    return datetime.date(year, 1, 1), datetime.date(year, 12, 31)


def month_period(year: int, month: int) -> tuple[datetime.date, datetime.date]:
    last = calendar.monthrange(year, month)[1]
    return datetime.date(year, month, 1), datetime.date(year, month, last)


def column_digest(columns: Iterable[str]) -> str:
    return hashlib.sha256("\n".join(sorted(columns)).encode("utf-8")).hexdigest()


def read_bytes(ref: RawRef) -> bytes:
    return pathlib.Path(ref.path).read_bytes()


def by_name(refs: Sequence[RawRef]) -> dict[str, RawRef]:
    return {pathlib.Path(ref.path).name: ref for ref in refs}


def only_ref(refs: Sequence[RawRef]) -> RawRef:
    if len(refs) != 1:
        raise SchemaChanged(f"expected one file, got {len(refs)}")
    return refs[0]


def decode(data: bytes, what: str) -> str:
    try:
        return data.decode("utf-8-sig")
    except UnicodeDecodeError as exc:
        raise SchemaChanged(f"{what} is not UTF-8: {exc}") from exc


def csv_header(data: bytes) -> list[str]:
    reader = csv.reader(io.StringIO(decode(data, "CSV file"), newline=""))
    try:
        return next(reader, [])
    except csv.Error as exc:
        raise SchemaChanged(f"unreadable CSV header: {exc}") from exc


def csv_rows(data: bytes, required: Iterable[str]) -> Iterator[dict[str, Any]]:
    """The rows of a CSV file, after checking that every required column is there."""
    text = decode(data, "CSV file")
    reader = csv.DictReader(io.StringIO(text, newline=""))
    try:
        fields = reader.fieldnames or []
        for column in required:
            if column not in fields:
                raise SchemaChanged(f"missing column {column}")
        yield from reader
    except csv.Error as exc:
        raise SchemaChanged(f"unreadable CSV file: {exc}") from exc


def load_json(data: bytes, what: str) -> Any:
    try:
        return json.loads(decode(data, what))
    except json.JSONDecodeError as exc:
        raise SchemaChanged(f"{what} is not JSON: {exc}") from exc


def only_csv_in_zip(data: bytes) -> bytes:
    try:
        with zipfile.ZipFile(io.BytesIO(data)) as archive:
            names = [
                name
                for name in archive.namelist()
                if name.lower().endswith(".csv") and not name.startswith("__MACOSX/")
            ]
            if len(names) != 1:
                raise SchemaChanged(f"expected one CSV in the zip, found {names}")
            declared = archive.getinfo(names[0]).file_size
            if declared > MAX_ZIP_MEMBER_BYTES:
                raise SchemaChanged(f"{names[0]} in the zip declares {declared} bytes")
            return archive.read(names[0])
    except zipfile.BadZipFile as exc:
        raise SchemaChanged(f"not a zip file: {exc}") from exc


def description_version(data: bytes) -> str:
    """The Version field of an R package DESCRIPTION file."""
    found = re.search(r"^Version:\s*(\S+)", decode(data, "DESCRIPTION"), re.MULTILINE)
    if found is None:
        raise SchemaChanged("missing column Version in DESCRIPTION")
    return found.group(1)


def highest_link(page: bytes, page_url: str, pattern: re.Pattern[str]) -> tuple[str, re.Match[str]]:
    """The link on a page whose path matches, taking the numerically highest of its groups."""
    found = page_link(page, page_url, pattern)
    if found is None:
        raise SchemaChanged(f"no link matching {pattern.pattern} on {page_url}")
    return found


def page_link(
    page: bytes, page_url: str, pattern: re.Pattern[str]
) -> tuple[str, re.Match[str]] | None:
    best: tuple[tuple[int, ...], str, re.Match[str]] | None = None
    html = page.decode("utf-8", errors="replace")
    page_host = urllib.parse.urlsplit(page_url).hostname
    for href in re.findall(r"""href\s*=\s*["']([^"']+)["']""", html):
        try:
            url = urllib.parse.urljoin(page_url, href)
            parts = urllib.parse.urlsplit(url)
        except ValueError:
            continue
        if parts.scheme not in ("https", "http") or parts.hostname != page_host:
            continue
        match = pattern.search(parts.path)
        if match is None:
            continue
        key = tuple(int(group) for group in match.groups())
        if best is None or key > best[0]:
            best = (key, url, match)
    return None if best is None else (best[1], best[2])


def basename(url: str) -> str:
    return urllib.parse.urlsplit(url).path.rsplit("/", 1)[-1]
