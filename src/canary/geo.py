"""Country names to ISO alpha-3 codes: exact matches only, never a guess."""

from __future__ import annotations

import csv
import hashlib
import json
import pathlib
from collections.abc import Mapping
from typing import Any

from sqlalchemy import select
from sqlalchemy.orm import Session

from canary.errors import SchemaChanged
from canary.schema import place

ALIASES_PATH = pathlib.Path(__file__).parents[2] / "reference" / "country_aliases.csv"


def _fold(name: str) -> str:
    return name.strip().casefold()


class CountryResolver:
    def __init__(self, names: Mapping[str, str], aliases: Mapping[str, str]) -> None:
        self._names = {_fold(name): code for name, code in names.items()}
        self._aliases = {_fold(name): code for name, code in aliases.items()}

    def resolve(self, name: str) -> str | None:
        key = _fold(name)
        return self._names.get(key) or self._aliases.get(key)


def load_aliases(path: pathlib.Path = ALIASES_PATH) -> dict[str, str]:
    with path.open(encoding="utf-8", newline="") as stream:
        return {row["source_name"]: row["iso3"] for row in csv.DictReader(stream)}


def resolver_digest(session: Session) -> str:
    """What names a run could resolve: the place names with their ids, and the aliases."""
    names = sorted((row.name, row.id) for row in session.execute(select(place.c.id, place.c.name)))
    try:
        aliases: Any = sorted(load_aliases().items())
    except (OSError, ValueError, KeyError, csv.Error) as exc:
        aliases = f"unreadable alias file: {type(exc).__name__}"
    text = json.dumps([names, aliases], separators=(",", ":"))
    return hashlib.sha256(text.encode("utf-8")).hexdigest()


def load_resolver(session: Session) -> CountryResolver:
    names = {row.name: row.id for row in session.execute(select(place.c.id, place.c.name))}
    if not names:
        raise SchemaChanged("the place table is empty: ingest geonames first")
    return CountryResolver(names, load_aliases())
