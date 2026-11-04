"""Shared test configuration: `db` tests skip visibly when no database is named."""

from __future__ import annotations

import os

import pytest


def pytest_collection_modifyitems(config: pytest.Config, items: list[pytest.Item]) -> None:
    if os.environ.get("CANARY_TEST_DATABASE_URL"):
        return
    skip = pytest.mark.skip(reason="CANARY_TEST_DATABASE_URL is not set")
    for item in items:
        if item.get_closest_marker("db"):
            item.add_marker(skip)
