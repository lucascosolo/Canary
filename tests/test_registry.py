"""Source registry loader: model rules, policy invariants, error reporting and the CLI."""

from __future__ import annotations

import datetime
import pathlib
from typing import Any

import pytest
import yaml
from pydantic import ValidationError

from canary.cli import main
from canary.registry import RegistryError, SourceEntry, load_registry

TODAY = datetime.date(2026, 11, 4)


def entry(**overrides: Any) -> dict[str, Any]:
    """One valid entry; a value of `...` removes that key."""
    data: dict[str, Any] = {
        "id": "example-source",
        "name": "Example Source",
        "organisation": "Example Org",
        "homepage": "https://example.org",
        "type": "api",
        "domains": ["economy"],
        "countries": "global",
        "languages": ["en"],
        "declared_cadence": "daily",
        "revision_policy": "none",
        "access_method": "REST",
        "auth": "none",
        "licence_id": "CC-BY-4.0",
        "terms_url": "https://example.org/terms",
        "terms_verified_on": datetime.date(2026, 11, 1),
        "canary_use": "open",
        "attribution_text": "Example Org",
        "source_class": "intergovernmental",
        "status": "lead",
    }
    data.update(overrides)
    return {k: v for k, v in data.items() if v is not ...}


def write(directory: pathlib.Path, data: dict[str, Any], name: str | None = None) -> pathlib.Path:
    path = directory / (name or f"{data['id']}.yaml")
    path.write_text(yaml.safe_dump(data), encoding="utf-8")
    return path


def problems_of(directory: pathlib.Path) -> list[str]:
    with pytest.raises(RegistryError) as info:
        load_registry(directory, today=TODAY)
    return info.value.problems


def load_one(tmp_path: pathlib.Path, **overrides: Any) -> SourceEntry:
    write(tmp_path, entry(**overrides))
    return load_registry(tmp_path, today=TODAY)[0]


def reject_one(tmp_path: pathlib.Path, **overrides: Any) -> list[str]:
    path = write(tmp_path, entry(**overrides), name="example-source.yaml")
    problems = problems_of(tmp_path)
    assert problems
    assert all(path.name in p for p in problems)
    return problems


# --- loading ---------------------------------------------------------------


def test_valid_entry_loads(tmp_path: pathlib.Path) -> None:
    loaded = load_one(tmp_path)
    assert isinstance(loaded, SourceEntry)
    assert loaded.id == "example-source"
    assert loaded.terms_verified_on == datetime.date(2026, 11, 1)
    assert loaded.endpoint is None
    assert loaded.expected_lag_days is None
    assert loaded.adapter is None


def test_results_sorted_by_id(tmp_path: pathlib.Path) -> None:
    for source_id in ("b-src", "c-src", "a-src"):
        write(tmp_path, entry(id=source_id))
    assert [e.id for e in load_registry(tmp_path, today=TODAY)] == ["a-src", "b-src", "c-src"]


def test_empty_directory_returns_empty_list(tmp_path: pathlib.Path) -> None:
    assert load_registry(tmp_path, today=TODAY) == []


def test_missing_directory_raises(tmp_path: pathlib.Path) -> None:
    missing = tmp_path / "nope"
    with pytest.raises(RegistryError) as info:
        load_registry(missing, today=TODAY)
    assert info.value.problems


def test_only_yaml_files_are_read(tmp_path: pathlib.Path) -> None:
    write(tmp_path, entry())
    (tmp_path / "notes.txt").write_text("not: [valid", encoding="utf-8")
    (tmp_path / "other.yml").write_text("- not a mapping", encoding="utf-8")
    assert [e.id for e in load_registry(tmp_path, today=TODAY)] == ["example-source"]


def test_today_defaults_to_current_date(tmp_path: pathlib.Path) -> None:
    write(tmp_path, entry(terms_verified_on=datetime.date(2020, 1, 1)))
    assert len(load_registry(tmp_path)) == 1


def test_file_name_must_equal_id(tmp_path: pathlib.Path) -> None:
    write(tmp_path, entry(id="real-id"), name="other-name.yaml")
    assert any("other-name.yaml" in p for p in problems_of(tmp_path))


def test_unknown_key_rejected(tmp_path: pathlib.Path) -> None:
    reject_one(tmp_path, surprise="x")


def test_source_entry_is_frozen(tmp_path: pathlib.Path) -> None:
    loaded = load_one(tmp_path)
    with pytest.raises(ValidationError):
        loaded.name = "Changed"  # type: ignore[misc]


# --- field rules -----------------------------------------------------------


@pytest.mark.parametrize(
    ("field", "bad"),
    [
        ("type", "spreadsheet"),
        ("revision_policy", "sometimes"),
        ("auth", "oauth"),
        ("canary_use", "free"),
        ("source_class", "blog"),
        ("status", "dreaming"),
    ],
)
def test_enumeration_rejects_bad_value(tmp_path: pathlib.Path, field: str, bad: str) -> None:
    reject_one(tmp_path, **{field: bad})


def test_domains_rejects_bad_member_and_empty(tmp_path: pathlib.Path) -> None:
    reject_one(tmp_path, domains=["economy", "weather"])
    reject_one(tmp_path, domains=[])


@pytest.mark.parametrize(
    "bad_id",
    ["Upper", "-leading", "has_underscore", "has space", ""],
)
def test_id_pattern_rejects(tmp_path: pathlib.Path, bad_id: str) -> None:
    write(tmp_path, entry(id=bad_id), name="x.yaml")
    assert any("x.yaml" in p for p in problems_of(tmp_path))


@pytest.mark.parametrize("homepage", ["ftp://example.org", "example.org"])
def test_homepage_must_be_http(tmp_path: pathlib.Path, homepage: str) -> None:
    reject_one(tmp_path, homepage=homepage)


def test_http_homepage_accepted(tmp_path: pathlib.Path) -> None:
    assert load_one(tmp_path, homepage="http://example.org").homepage == "http://example.org"


@pytest.mark.parametrize("field", ["name", "organisation", "declared_cadence", "access_method"])
def test_non_empty_strings(tmp_path: pathlib.Path, field: str) -> None:
    reject_one(tmp_path, **{field: ""})


@pytest.mark.parametrize("countries", ["global", ["USA"], ["USA", "GBR"]])
def test_countries_accepts(tmp_path: pathlib.Path, countries: Any) -> None:
    assert load_one(tmp_path, countries=countries).countries == countries


@pytest.mark.parametrize("countries", ["usa", "USA", ["usa"], ["US"], ["USAA"], [], "Global"])
def test_countries_rejects(tmp_path: pathlib.Path, countries: Any) -> None:
    reject_one(tmp_path, countries=countries)


@pytest.mark.parametrize("languages", [["en"], ["eng"], ["en", "fra"]])
def test_languages_accepts(tmp_path: pathlib.Path, languages: list[str]) -> None:
    assert list(load_one(tmp_path, languages=languages).languages) == languages


@pytest.mark.parametrize("languages", [["EN"], ["e"], ["engl"], ["e1"], []])
def test_languages_rejects(tmp_path: pathlib.Path, languages: list[str]) -> None:
    reject_one(tmp_path, languages=languages)


def test_expected_lag_days(tmp_path: pathlib.Path) -> None:
    assert load_one(tmp_path, expected_lag_days=0).expected_lag_days == 0
    other = tmp_path / "neg"
    other.mkdir()
    reject_one(other, expected_lag_days=-1)


def test_terms_verified_on_not_after_today(tmp_path: pathlib.Path) -> None:
    assert load_one(tmp_path, terms_verified_on=TODAY).terms_verified_on == TODAY
    other = tmp_path / "future"
    other.mkdir()
    reject_one(other, terms_verified_on=TODAY + datetime.timedelta(days=1))


# --- optionality tied to canary_use ----------------------------------------

TERMS_FIELDS = ["licence_id", "terms_url", "terms_verified_on"]


def test_terms_fields_optional_when_unverified(tmp_path: pathlib.Path) -> None:
    loaded = load_one(
        tmp_path,
        canary_use="unverified",
        attribution_text=...,
        licence_id=...,
        terms_url=...,
        terms_verified_on=...,
    )
    assert loaded.licence_id is None
    assert loaded.terms_url is None
    assert loaded.terms_verified_on is None


@pytest.mark.parametrize("field", TERMS_FIELDS)
@pytest.mark.parametrize("use", ["open", "display", "links", "permission", "excluded"])
def test_terms_fields_required_otherwise(tmp_path: pathlib.Path, field: str, use: str) -> None:
    reject_one(tmp_path, canary_use=use, attribution_text="Example", **{field: ...})


@pytest.mark.parametrize("use", ["open", "display"])
def test_attribution_required_for_open_and_display(tmp_path: pathlib.Path, use: str) -> None:
    reject_one(tmp_path, canary_use=use, attribution_text=...)
    other = tmp_path / "empty"
    other.mkdir()
    reject_one(other, canary_use=use, attribution_text="")


@pytest.mark.parametrize("use", ["links", "permission", "excluded", "unverified"])
def test_attribution_optional_otherwise(tmp_path: pathlib.Path, use: str) -> None:
    assert load_one(tmp_path, canary_use=use, attribution_text=...).attribution_text is None


# --- policy invariants -----------------------------------------------------

INTEGRATED: dict[str, Any] = {
    "status": "integrated",
    "auth": "none",
    "canary_use": "open",
    "adapter": "example_adapter",
    "integrated_on": datetime.date(2026, 11, 2),
}


def test_integrated_valid(tmp_path: pathlib.Path) -> None:
    assert load_one(tmp_path, **INTEGRATED).status == "integrated"


def test_integrated_display_valid(tmp_path: pathlib.Path) -> None:
    assert load_one(tmp_path, **{**INTEGRATED, "canary_use": "display"}).status == "integrated"


@pytest.mark.parametrize(
    "broken",
    [
        {"auth": "key"},
        {"canary_use": "links"},
        {"canary_use": "unverified", "licence_id": ..., "terms_url": ..., "terms_verified_on": ...},
        {"adapter": ...},
        {"adapter": ""},
        {"integrated_on": ...},
    ],
    ids=["auth", "canary_use", "unverified", "adapter-missing", "adapter-empty", "integrated_on"],
)
def test_integrated_invariant_failures(tmp_path: pathlib.Path, broken: dict[str, Any]) -> None:
    reject_one(tmp_path, **{**INTEGRATED, **broken})


def test_retired_valid(tmp_path: pathlib.Path) -> None:
    loaded = load_one(
        tmp_path,
        status="retired",
        retired_on=datetime.date(2026, 10, 1),
        retired_reason="Shut down",
    )
    assert loaded.retired_reason == "Shut down"


@pytest.mark.parametrize("missing", ["retired_on", "retired_reason"])
def test_retired_requires_fields(tmp_path: pathlib.Path, missing: str) -> None:
    fields = {"retired_on": datetime.date(2026, 10, 1), "retired_reason": "Shut down"}
    fields.pop(missing)
    reject_one(tmp_path, status="retired", **fields)


def test_evaluated_requires_evaluated_on(tmp_path: pathlib.Path) -> None:
    ok = load_one(tmp_path, status="evaluated", evaluated_on=datetime.date(2026, 10, 1))
    assert ok.evaluated_on == datetime.date(2026, 10, 1)
    other = tmp_path / "missing"
    other.mkdir()
    reject_one(other, status="evaluated")


# --- error reporting -------------------------------------------------------


def test_invalid_yaml_and_non_mapping_reported_with_other_bad_files(
    tmp_path: pathlib.Path,
) -> None:
    (tmp_path / "broken.yaml").write_text("id: [unclosed\n  - x: : :", encoding="utf-8")
    (tmp_path / "listy.yaml").write_text("- a\n- b\n", encoding="utf-8")
    write(tmp_path, entry(id="bad-enum", status="dreaming"))
    write(tmp_path, entry(id="fine"))
    problems = problems_of(tmp_path)
    for name in ("broken.yaml", "listy.yaml", "bad-enum.yaml"):
        assert any(name in p for p in problems), name
    assert not any("fine.yaml" in p for p in problems)


def test_all_problems_in_one_file_are_not_required_but_every_problem_names_a_file(
    tmp_path: pathlib.Path,
) -> None:
    write(tmp_path, entry(id="one", auth="oauth"))
    write(tmp_path, entry(id="two", type="nope"))
    problems = problems_of(tmp_path)
    assert all(("one.yaml" in p) or ("two.yaml" in p) for p in problems)
    assert any("one.yaml" in p for p in problems)
    assert any("two.yaml" in p for p in problems)


# --- CLI -------------------------------------------------------------------


def test_cli_validate_success(tmp_path: pathlib.Path, capsys: pytest.CaptureFixture[str]) -> None:
    write(tmp_path, entry(id="a-src"))
    write(tmp_path, entry(id="b-src"))
    assert main(["registry", "validate", "--path", str(tmp_path)]) == 0
    assert "2 sources valid" in capsys.readouterr().out


def test_cli_validate_failure(tmp_path: pathlib.Path, capsys: pytest.CaptureFixture[str]) -> None:
    write(tmp_path, entry(id="bad-one", status="dreaming"))
    write(tmp_path, entry(id="bad-two", type="nope"))
    assert main(["registry", "validate", "--path", str(tmp_path)]) == 1
    captured = capsys.readouterr()
    lines = [line for line in captured.err.splitlines() if line.strip()]
    assert any("bad-one.yaml" in line for line in lines)
    assert any("bad-two.yaml" in line for line in lines)
    assert "valid" not in captured.out
