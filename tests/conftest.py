"""Shared test configuration.

`db` tests get a real PostgreSQL. CANARY_TEST_DATABASE_URL wins when set. Otherwise a throwaway
server starts in pytest's temporary directory and stops at the end of the session. They skip,
visibly, only when neither is possible.
"""

from __future__ import annotations

import os
from collections.abc import Iterator

import pytest
from alembic import command
from alembic.config import Config
from sqlalchemy import Engine, create_engine
from sqlalchemy.orm import Session

from canary import devdb


def pytest_collection_modifyitems(config: pytest.Config, items: list[pytest.Item]) -> None:
    if os.environ.get("CANARY_TEST_DATABASE_URL") or devdb.available():
        return
    skip = pytest.mark.skip(reason="no CANARY_TEST_DATABASE_URL and no PostgreSQL 17 binaries")
    for item in items:
        if item.get_closest_marker("db"):
            item.add_marker(skip)


@pytest.fixture(scope="session")
def database_url(tmp_path_factory: pytest.TempPathFactory) -> Iterator[str]:
    """An empty database for this test session, with no migrations applied."""
    external = os.environ.get("CANARY_TEST_DATABASE_URL")
    if external:
        yield external
        return
    server = devdb.LocalServer(
        tmp_path_factory.mktemp("pg") / "data", devdb.free_port(), durable=False
    )
    server.start()
    try:
        yield server.create_database("canary_test")
    finally:
        server.stop()


@pytest.fixture(scope="session")
def migrated_engine(database_url: str, monkeypatch_session: pytest.MonkeyPatch) -> Iterator[Engine]:
    """An engine on a database migrated to head."""
    monkeypatch_session.setenv("CANARY_DATABASE_URL", database_url)
    command.upgrade(Config("alembic.ini"), "head")
    engine = create_engine(database_url)
    yield engine
    engine.dispose()


@pytest.fixture(scope="session")
def monkeypatch_session() -> Iterator[pytest.MonkeyPatch]:
    with pytest.MonkeyPatch.context() as patch:
        yield patch


@pytest.fixture
def db_session(migrated_engine: Engine) -> Iterator[Session]:
    """A session whose work is rolled back after the test, including nested commits."""
    with migrated_engine.connect() as connection:
        transaction = connection.begin()
        session = Session(bind=connection, join_transaction_mode="create_savepoint")
        try:
            yield session
        finally:
            session.close()
            transaction.rollback()
