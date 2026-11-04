"""The `canary` command line."""

from __future__ import annotations

import argparse
import pathlib
import sys
from collections.abc import Sequence

from canary import __version__
from canary.registry import RegistryError, load_registry


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(prog="canary", description=__doc__)
    parser.add_argument("--version", action="version", version=f"canary {__version__}")
    commands = parser.add_subparsers(dest="command")
    registry = commands.add_parser("registry", help="source registry commands")
    registry_commands = registry.add_subparsers(dest="registry_command", required=True)
    validate = registry_commands.add_parser("validate", help="validate the source registry")
    validate.add_argument("--path", type=pathlib.Path, default=pathlib.Path("registry"))
    return parser


def main(argv: Sequence[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    if args.command == "registry":
        try:
            entries = load_registry(args.path)
        except RegistryError as exc:
            for problem in exc.problems:
                print(problem, file=sys.stderr)
            return 1
        print(f"{len(entries)} sources valid")
    return 0
