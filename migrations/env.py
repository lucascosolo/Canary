"""Alembic environment. The database is named by CANARY_DATABASE_URL, never by a file."""

from __future__ import annotations

import os

from alembic import context
from sqlalchemy import create_engine

OFFLINE_URL = "postgresql+psycopg://"

target_metadata = None


def run_offline() -> None:
    url = os.environ.get("CANARY_DATABASE_URL", OFFLINE_URL)
    context.configure(url=url, target_metadata=target_metadata, literal_binds=True)
    with context.begin_transaction():
        context.run_migrations()


def run_online() -> None:
    url = os.environ.get("CANARY_DATABASE_URL")
    if not url:
        raise SystemExit("CANARY_DATABASE_URL is not set")
    with create_engine(url).connect() as connection:
        context.configure(connection=connection, target_metadata=target_metadata)
        with context.begin_transaction():
            context.run_migrations()


if context.is_offline_mode():
    run_offline()
else:
    run_online()
