"""The `canary` command line."""

from __future__ import annotations

import argparse
import hashlib
import os
import pathlib
import subprocess
import sys
from collections.abc import Sequence

from sqlalchemy import create_engine
from sqlalchemy.orm import Session

from canary import __version__
from canary.provenance import entry_digest, finish_run, health_report, start_run, sync_registry
from canary.registry import RegistryError, load_registry


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
    return parser


def _database_url() -> str | None:
    url = os.environ.get("CANARY_DATABASE_URL")
    if not url:
        print("CANARY_DATABASE_URL is not set", file=sys.stderr)
    return url


def _code_commit() -> str:
    result = subprocess.run(["git", "rev-parse", "HEAD"], capture_output=True, text=True)
    return result.stdout.strip() if result.returncode == 0 and result.stdout.strip() else "unknown"


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
            session, "ingest", code_commit=_code_commit(), config_digest=config_digest
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


def _health() -> int:
    url = _database_url()
    if url is None:
        return 2
    engine = create_engine(url)
    with Session(engine) as session:
        rows = health_report(session)
    engine.dispose()
    for row in rows:
        last_ok = row.last_ok_at.isoformat() if row.last_ok_at else "never"
        print(f"{row.source_id} {row.freshness} {last_ok}")
    return 0


def main(argv: Sequence[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
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
