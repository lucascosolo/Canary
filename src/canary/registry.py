"""Source registry loader: one YAML file per source, validated against docs/03 sections 7 and 8."""

from __future__ import annotations

import datetime
import pathlib
from typing import Annotated, Literal

import yaml
from pydantic import BaseModel, ConfigDict, Field, ValidationError, ValidationInfo, model_validator

NonEmpty = Annotated[str, Field(min_length=1)]
Url = Annotated[str, Field(pattern=r"^https?://")]
CountryCode = Annotated[str, Field(pattern=r"^[A-Z]{3}$")]
LanguageCode = Annotated[str, Field(pattern=r"^[a-z]{2,3}$")]

Domain = Literal[
    "institutions",
    "elections",
    "legislation",
    "conflict",
    "rights",
    "information",
    "economy",
    "humanitarian",
    "reference",
]
SourceType = Literal[
    "index", "event_dataset", "api", "rss", "document_feed", "catalog", "reference", "model_output"
]
CanaryUse = Literal["open", "display", "links", "permission", "excluded", "unverified"]
SourceClass = Literal[
    "official_government",
    "intergovernmental",
    "ngo_advocacy",
    "ngo_documentation",
    "academic",
    "media_wire",
    "media_national",
    "media_local",
    "state_media",
    "platform",
    "model_output",
]


class RegistryError(Exception):
    def __init__(self, problems: list[str]) -> None:
        super().__init__("; ".join(problems))
        self.problems = problems


class SourceEntry(BaseModel):
    model_config = ConfigDict(frozen=True, extra="forbid")

    id: Annotated[str, Field(pattern=r"^[a-z0-9][a-z0-9-]*$")]
    name: NonEmpty
    organisation: NonEmpty
    homepage: Url
    type: SourceType
    domains: Annotated[list[Domain], Field(min_length=1)]
    countries: Literal["global"] | Annotated[list[CountryCode], Field(min_length=1)]
    languages: Annotated[list[LanguageCode], Field(min_length=1)]
    declared_cadence: NonEmpty
    expected_lag_days: Annotated[int, Field(ge=0)] | None = None
    revision_policy: Literal["none", "silent", "announced"]
    access_method: NonEmpty
    endpoint: str | None = None
    auth: Literal["none", "key", "token_by_request", "account", "credentials_by_request"]
    rate_limit_text: str | None = None
    adapter: str | None = None
    licence_id: str | None = None
    terms_url: str | None = None
    terms_verified_on: datetime.date | None = None
    canary_use: CanaryUse
    attribution_text: str | None = None
    redistribution_notes: str | None = None
    source_class: SourceClass
    state_control_class: str | None = None
    funding_notes: str | None = None
    quality_notes: str | None = None
    status: Literal["lead", "evaluated", "integrated", "degraded", "retired"]
    evaluated_on: datetime.date | None = None
    integrated_on: datetime.date | None = None
    retired_on: datetime.date | None = None
    retired_reason: str | None = None

    @model_validator(mode="after")
    def _check_policy(self, info: ValidationInfo) -> SourceEntry:
        today = (info.context or {}).get("today") or datetime.date.today()
        errors: list[str] = []
        if self.canary_use != "unverified":
            for field in ("licence_id", "terms_url", "terms_verified_on"):
                if getattr(self, field) is None:
                    errors.append(f"{field} is required unless canary_use is unverified")
        if self.terms_verified_on is not None and self.terms_verified_on > today:
            errors.append("terms_verified_on is after today")
        if self.canary_use in ("open", "display") and not self.attribution_text:
            errors.append("attribution_text is required when canary_use is open or display")
        if self.status == "integrated":
            if self.auth != "none":
                errors.append("integrated requires auth none")
            if self.canary_use not in ("open", "display"):
                errors.append("integrated requires canary_use open or display")
            if not self.adapter:
                errors.append("integrated requires a non-empty adapter")
            if self.integrated_on is None:
                errors.append("integrated requires integrated_on")
        if self.status == "retired" and (self.retired_on is None or self.retired_reason is None):
            errors.append("retired requires retired_on and retired_reason")
        if self.status == "evaluated" and self.evaluated_on is None:
            errors.append("evaluated requires evaluated_on")
        if errors:
            raise ValueError("; ".join(errors))
        return self


def _load_file(path: pathlib.Path, today: datetime.date) -> tuple[SourceEntry | None, list[str]]:
    try:
        data = yaml.safe_load(path.read_text(encoding="utf-8"))
    except (yaml.YAMLError, UnicodeDecodeError) as exc:
        return None, [f"{path.name}: cannot parse YAML: {exc}".replace("\n", " ")]
    if not isinstance(data, dict):
        return None, [f"{path.name}: top level must be a mapping"]
    try:
        entry = SourceEntry.model_validate(data, context={"today": today})
    except ValidationError as exc:
        return None, [
            f"{path.name}: {'.'.join(str(p) for p in e['loc']) or 'entry'}: {e['msg']}"
            for e in exc.errors()
        ]
    if entry.id != path.stem:
        return None, [f"{path.name}: id {entry.id!r} does not match the file name"]
    return entry, []


def load_registry(
    directory: pathlib.Path, today: datetime.date | None = None
) -> list[SourceEntry]:
    if not directory.is_dir():
        raise RegistryError([f"{directory}: registry directory not found"])
    today = today or datetime.date.today()
    entries: list[SourceEntry] = []
    problems: list[str] = []
    for path in sorted(directory.glob("*.yaml")):
        entry, found = _load_file(path, today)
        if entry is not None:
            entries.append(entry)
        problems.extend(found)
    if problems:
        raise RegistryError(problems)
    return sorted(entries, key=lambda e: e.id)
