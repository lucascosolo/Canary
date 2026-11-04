"""The ingestion runner: one source, one pipeline run, one health record. Nothing here commits."""

from __future__ import annotations

import hashlib
import pathlib
import subprocess
import uuid
from collections.abc import Iterable
from dataclasses import dataclass
from typing import Any

from sqlalchemy import select, update
from sqlalchemy.dialects.postgresql import insert as pg_insert
from sqlalchemy.orm import Session

from canary.adapters.base import Adapter, ParseResult, PlaceRow
from canary.errors import AccessRefused, FetchFailed, ManualFileMissing, NotPermitted, SchemaChanged
from canary.geo import load_resolver
from canary.http import Fetcher
from canary.observations import sync_indicator, write_observations
from canary.provenance import finish_run, record_health, record_release, start_run
from canary.rawstore import RawRef, RawStore
from canary.schema import place, source

PERMITTED_USES = ("open", "display")
RECORDED_FAILURES = (AccessRefused, FetchFailed, ManualFileMissing, SchemaChanged)


@dataclass(frozen=True)
class IngestResult:
    source_id: str
    version_label: str
    new_release: bool
    written: int
    unchanged: int
    skipped: int
    unmapped: int


def code_commit() -> str:
    result = subprocess.run(["git", "rev-parse", "HEAD"], capture_output=True, text=True)
    return result.stdout.strip() if result.returncode == 0 and result.stdout.strip() else "unknown"


def content_digest(refs: Iterable[RawRef]) -> str:
    lines = sorted(f"{pathlib.Path(ref.path).name}:{ref.sha256}" for ref in refs)
    return hashlib.sha256("\n".join(lines).encode("utf-8")).hexdigest()


def _licence_snapshot(record: dict[str, Any]) -> str:
    return (
        f"{record['licence_id']} ({record['terms_url']}, verified {record['terms_verified_on']})"
    )


def _file_refs(refs: Iterable[RawRef]) -> list[dict[str, Any]]:
    return [
        {
            "filename": pathlib.Path(ref.path).name,
            "sha256": ref.sha256,
            "size_bytes": ref.size_bytes,
        }
        for ref in refs
    ]


def _upsert_places(session: Session, rows: Iterable[PlaceRow], run_id: uuid.UUID) -> None:
    for row in rows:
        fields = {
            "iso2": row.iso2,
            "name": row.name,
            "continent": row.continent,
            "geonames_id": row.geonames_id,
            "run_id": run_id,
        }
        session.execute(
            pg_insert(place)
            .values(id=row.id, **fields)
            .on_conflict_do_update(index_elements=["id"], set_=fields)
        )


def _link_wikidata(session: Session, links: dict[str, str], run_id: uuid.UUID) -> None:
    for code, item in sorted(links.items()):
        session.execute(
            update(place).where(place.c.id == code).values(wikidata_id=item, run_id=run_id)
        )


def _write(
    session: Session,
    adapter: Adapter,
    parsed: ParseResult,
    refs: list[RawRef],
    ref: Any,
    digest: str,
    licence: str,
    run_id: uuid.UUID,
) -> tuple[bool, int, int]:
    release_id, new_release = record_release(
        session,
        adapter.source_id,
        version_label=ref.version_label,
        content_digest=digest,
        row_count=parsed.parsed_count,
        schema_digest=parsed.schema_digest,
        licence_snapshot=licence,
        file_refs=_file_refs(refs),
        run_id=run_id,
        released_at=ref.released_at,
    )
    for spec in parsed.indicators:
        sync_indicator(session, spec)
    try:
        outcome = write_observations(session, release_id, run_id, parsed.rows)
    except ValueError as exc:
        raise SchemaChanged(f"{adapter.source_id}: {exc}") from exc
    _upsert_places(session, parsed.places, run_id)
    _link_wikidata(session, parsed.wikidata_ids, run_id)
    return new_release, outcome.written, outcome.unchanged


def _ingest_steps(
    session: Session,
    adapter: Adapter,
    fetcher: Fetcher,
    store: RawStore,
    licence: str,
    run_id: uuid.UUID,
) -> IngestResult:
    source_id = adapter.source_id
    resolver = load_resolver(session) if adapter.needs_resolver else None
    ref = adapter.discover(fetcher)
    if not ref.urls:
        record_health(session, source_id, ok=True, items_seen=0)
        finish_run(session, run_id, notes="nothing to fetch")
        return IngestResult(source_id, ref.version_label, False, 0, 0, 0, 0)
    refs = adapter.fetch(fetcher, ref, store)
    digest = content_digest(refs)
    with session.begin_nested():
        parsed = adapter.parse(refs, resolver)
        new_release, written, unchanged = _write(
            session, adapter, parsed, refs, ref, digest, licence, run_id
        )
    record_health(
        session,
        source_id,
        ok=True,
        items_seen=parsed.parsed_count,
        schema_digest=parsed.schema_digest,
    )
    finish_run(
        session,
        run_id,
        input_count=parsed.parsed_count + parsed.skipped,
        output_count=written + len(parsed.places) + len(parsed.wikidata_ids),
        notes="unmapped: " + "; ".join(parsed.unmapped) if parsed.unmapped else None,
    )
    return IngestResult(
        source_id,
        ref.version_label,
        new_release,
        written,
        unchanged,
        parsed.skipped,
        len(parsed.unmapped),
    )


def ingest(session: Session, adapter: Adapter, fetcher: Fetcher, store: RawStore) -> IngestResult:
    source_id = adapter.source_id
    registered = session.execute(
        select(source.c.canary_use, source.c.record).where(source.c.id == source_id)
    ).one_or_none()
    if registered is None:
        raise NotPermitted(f"{source_id} is not in the source table: run 'canary registry sync'")
    if registered.canary_use not in PERMITTED_USES:
        raise NotPermitted(f"{source_id} has canary_use {registered.canary_use}")
    licence = _licence_snapshot(registered.record)
    run_id = start_run(
        session, "ingest", code_commit=code_commit(), config_digest=adapter.config_digest()
    )
    try:
        return _ingest_steps(session, adapter, fetcher, store, licence, run_id)
    except RECORDED_FAILURES as exc:
        record_health(session, source_id, ok=False, message=str(exc))
        finish_run(session, run_id, error_count=1, notes=str(exc))
        raise
