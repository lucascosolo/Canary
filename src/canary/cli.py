"""The `canary` command line."""

from __future__ import annotations

import argparse
import datetime
import hashlib
import os
import pathlib
import sys
from collections.abc import Sequence

from alembic import command
from alembic.config import Config
from sqlalchemy import create_engine
from sqlalchemy.orm import Session

from canary import __version__, devdb
from canary.adapters import ADAPTERS
from canary.errors import (
    AccessRefused,
    FetchFailed,
    ManualFileMissing,
    NotPermitted,
    SchemaChanged,
)
from canary.http import Fetcher
from canary.ingest import code_commit, ingest
from canary.observations import table_counts
from canary.provenance import entry_digest, finish_run, health_report, start_run, sync_registry
from canary.rawstore import RawStore
from canary.registry import RegistryError, load_registry

REPORTED_FAILURES = (AccessRefused, FetchFailed, ManualFileMissing, SchemaChanged, NotPermitted)


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(prog="canary", description=__doc__)
    parser.add_argument("--version", action="version", version=f"canary {__version__}")
    commands = parser.add_subparsers(dest="command")
    registry = commands.add_parser("registry", help="source registry commands")
    registry_commands = registry.add_subparsers(dest="registry_command", required=True)
    validate = registry_commands.add_parser("validate", help="validate the source registry")
    validate.add_argument("--path", type=pathlib.Path, default=pathlib.Path("registry"))
    sync = registry_commands.add_parser("sync", help="record the source registry in the database")
    sync.add_argument("--path", type=pathlib.Path, default=pathlib.Path("registry"))
    commands.add_parser("health", help="report source freshness")
    commands.add_parser("status", help="row counts of every table")
    ingest_parser = commands.add_parser("ingest", help="ingest one source")
    ingest_parser.add_argument("source_id")
    database = commands.add_parser("db", help="the private development database")
    database.add_argument("action", choices=["start", "stop", "url"])
    return parser


def _database_url() -> str | None:
    url = os.environ.get("CANARY_DATABASE_URL")
    if not url:
        print("CANARY_DATABASE_URL is not set", file=sys.stderr)
    return url


def _ingest(source_id: str) -> int:
    url = _database_url()
    if url is None:
        return 2
    factory = ADAPTERS.get(source_id)
    if factory is None:
        print(f"unknown source: {source_id}", file=sys.stderr)
        return 1
    engine = create_engine(url)
    with Session(engine) as session:
        try:
            result = ingest(session, factory(), Fetcher(), RawStore())
        except REPORTED_FAILURES as exc:
            session.commit()
            print(f"{source_id}: {exc}", file=sys.stderr)
            engine.dispose()
            return 1
        session.commit()
    engine.dispose()
    state = "new" if result.new_release else "existing"
    print(
        f"{result.source_id} {result.version_label} {state} written={result.written} "
        f"unchanged={result.unchanged} skipped={result.skipped} unmapped={result.unmapped}"
    )
    return 0


def _db(action: str) -> int:
    server = devdb.dev_server()
    if action == "url":
        print(server.url("canary"))
    elif action == "stop":
        server.stop()
    else:
        server.start()
        if not server.database_exists("canary"):
            server.create_database("canary")
        os.environ["CANARY_DATABASE_URL"] = server.url("canary")
        command.upgrade(Config("alembic.ini"), "head")
    return 0


def _registry_sync(path: pathlib.Path) -> int:
    url = _database_url()
    if url is None:
        return 2
    try:
        entries = load_registry(path)
    except RegistryError as exc:
        for problem in exc.problems:
            print(problem, file=sys.stderr)
        return 1
    digests = sorted(entry_digest(entry) for entry in entries)
    config_digest = hashlib.sha256("".join(digests).encode("utf-8")).hexdigest()
    engine = create_engine(url)
    with Session(engine) as session:
        run_id = start_run(
            session, "ingest", code_commit=code_commit(), config_digest=config_digest
        )
        result = sync_registry(session, entries, run_id=run_id)
        finish_run(session, run_id, input_count=len(entries), output_count=len(result.added))
        session.commit()
    engine.dispose()
    print(
        f"added {len(result.added)}, changed {len(result.changed)}, "
        f"unchanged {len(result.unchanged)}, missing {len(result.missing)}"
    )
    return 0


def _status() -> int:
    url = _database_url()
    if url is None:
        return 2
    engine = create_engine(url)
    with Session(engine) as session:
        counts = table_counts(session)
    engine.dispose()
    for table in sorted(counts):
        print(f"{table} {counts[table]}")
    return 0


def _health() -> int:
    url = _database_url()
    if url is None:
        return 2
    engine = create_engine(url)
    with Session(engine) as session:
        rows = health_report(session)
    engine.dispose()
    for row in rows:
        last_ok = row.last_ok_at.astimezone(datetime.UTC).isoformat() if row.last_ok_at else "never"
        print(f"{row.source_id} {row.freshness} {last_ok}")
    return 0


def main(argv: Sequence[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    if args.command == "ingest":
        return _ingest(args.source_id)
    if args.command == "db":
        return _db(args.action)
    if args.command == "status":
        return _status()
    if args.command == "health":
        return _health()
    if args.command == "registry" and args.registry_command == "sync":
        return _registry_sync(args.path)
    if args.command == "registry":
        try:
            entries = load_registry(args.path)
        except RegistryError as exc:
            for problem in exc.problems:
                print(problem, file=sys.stderr)
            return 1
        print(f"{len(entries)} sources valid")
    return 0
