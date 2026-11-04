"""A private PostgreSQL server for development and tests on this PC.

It listens on TCP at 127.0.0.1 only, because the agent sandbox refuses Unix sockets. Authentication
is `trust`, so it must never be used outside a single-user development machine. This module starts
and stops servers; it never removes a data directory.
"""

from __future__ import annotations

import os
import pathlib
import socket
import subprocess

DEFAULT_PG_BIN = "/usr/lib/postgresql/17/bin"
DEV_PORT = 54320
USER = "canary"


def pg_bin() -> pathlib.Path:
    return pathlib.Path(os.environ.get("CANARY_PG_BIN", DEFAULT_PG_BIN))


def available() -> bool:
    return (pg_bin() / "pg_ctl").exists()


def free_port() -> int:
    with socket.socket() as sock:
        sock.bind(("127.0.0.1", 0))
        return sock.getsockname()[1]


def default_dev_dir() -> pathlib.Path:
    return pathlib.Path.home() / ".cache" / "canary" / "dev-pg"


class LocalServer:
    def __init__(self, data_dir: pathlib.Path, port: int, *, durable: bool = True) -> None:
        self.data_dir = data_dir
        self.port = port
        self.durable = durable

    def url(self, database: str = "postgres") -> str:
        return f"postgresql+psycopg://{USER}@127.0.0.1:{self.port}/{database}"

    def _run(self, *args: str) -> None:
        subprocess.run(args, check=True, capture_output=True, text=True)

    def _ctl(self, *args: str) -> None:
        self._run(str(pg_bin() / "pg_ctl"), "-D", str(self.data_dir), "-w", *args)

    def is_running(self) -> bool:
        status = subprocess.run(
            [str(pg_bin() / "pg_ctl"), "-D", str(self.data_dir), "status"],
            capture_output=True,
            text=True,
        )
        return status.returncode == 0

    def initialise(self) -> None:
        """Create the cluster if the directory has none. An existing cluster is left as it is."""
        if (self.data_dir / "PG_VERSION").exists():
            return
        self.data_dir.parent.mkdir(parents=True, exist_ok=True)
        self._run(
            str(pg_bin() / "initdb"),
            "-D",
            str(self.data_dir),
            "-U",
            USER,
            "-A",
            "trust",
            "-E",
            "UTF8",
            "--locale=C.UTF-8",
        )

    def start(self) -> None:
        self.initialise()
        if self.is_running():
            return
        options = f"-p {self.port} -c listen_addresses=127.0.0.1 -c unix_socket_directories=''"
        if not self.durable:
            options += " -c fsync=off -c synchronous_commit=off -c full_page_writes=off"
        self._ctl("-l", str(self.data_dir / "server.log"), "-o", options, "start")

    def stop(self) -> None:
        if self.is_running():
            self._ctl("-m", "fast", "stop")

    def _psql(self, sql: str) -> str:
        command = [
            str(pg_bin() / "psql"),
            "-h",
            "127.0.0.1",
            "-p",
            str(self.port),
            "-U",
            USER,
            "-d",
            "postgres",
            "-v",
            "ON_ERROR_STOP=1",
            "-tAc",
            sql,
        ]
        return subprocess.run(command, check=True, capture_output=True, text=True).stdout

    def database_exists(self, name: str) -> bool:
        if not name.replace("_", "").isalnum():
            raise ValueError(f"unsafe database name: {name!r}")
        return self._psql(f"SELECT 1 FROM pg_database WHERE datname = '{name}'").strip() == "1"

    def create_database(self, name: str) -> str:
        if not name.replace("_", "").isalnum():
            raise ValueError(f"unsafe database name: {name!r}")
        self._psql(f'CREATE DATABASE "{name}"')
        return self.url(name)


def dev_server() -> LocalServer:
    return LocalServer(default_dev_dir(), DEV_PORT)
