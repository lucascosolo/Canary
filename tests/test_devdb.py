import pathlib

import pytest
from sqlalchemy import Engine, create_engine, text

from canary import devdb

pytestmark = pytest.mark.db


def test_database_has_what_the_schema_needs(database_url: str) -> None:
    engine: Engine = create_engine(database_url)
    with engine.connect() as connection:
        version = connection.execute(text("show server_version_num")).scalar_one()
        assert version.startswith("17")
        connection.execute(text("create extension if not exists pg_trgm"))
        assert connection.execute(text("select similarity('court', 'courts') > 0.5")).scalar_one()
        connection.rollback()
    engine.dispose()


def test_migrations_reach_head(migrated_engine: Engine) -> None:
    with migrated_engine.connect() as connection:
        assert connection.execute(text("select version_num from alembic_version")).scalar_one()


def test_server_starts_twice_and_keeps_an_existing_cluster(tmp_path: pathlib.Path) -> None:
    server = devdb.LocalServer(tmp_path / "data", devdb.free_port(), durable=False)
    server.start()
    try:
        server.start()
        assert server.is_running()
        marker = (tmp_path / "data" / "PG_VERSION").stat().st_mtime_ns
        server.initialise()
        assert (tmp_path / "data" / "PG_VERSION").stat().st_mtime_ns == marker
    finally:
        server.stop()
    assert not server.is_running()


def test_unsafe_database_name_is_refused(tmp_path: pathlib.Path) -> None:
    with pytest.raises(ValueError):
        devdb.LocalServer(tmp_path / "data", 1).create_database('x"; drop table y; --')
