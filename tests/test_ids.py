"""Identifier generation: version 7 UUIDs that sort in time order."""

from __future__ import annotations

import time
import uuid

from canary.ids import new_id


def test_new_id_is_a_version_7_uuid() -> None:
    value = new_id()
    assert isinstance(value, uuid.UUID)
    assert value.version == 7


def test_ids_are_unique() -> None:
    assert len({new_id() for _ in range(1000)}) == 1000


def test_ids_a_millisecond_apart_sort_in_time_order() -> None:
    values = []
    for _ in range(5):
        values.append(new_id())
        time.sleep(0.005)
    assert values == sorted(values)
    assert [v.bytes for v in values] == sorted(v.bytes for v in values)
