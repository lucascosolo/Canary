"""Identifiers: version 7 UUIDs (RFC 9562), which sort in time order."""

from __future__ import annotations

import os
import time
import uuid


def new_id() -> uuid.UUID:
    """A version 7 UUID: 48-bit millisecond timestamp, then random bits."""
    milliseconds = time.time_ns() // 1_000_000
    value = (milliseconds & (2**48 - 1)) << 80
    value |= int.from_bytes(os.urandom(10)) & ((1 << 80) - 1)
    value = (value & ~(0xF << 76)) | (0x7 << 76)
    value = (value & ~(0x3 << 62)) | (0x2 << 62)
    return uuid.UUID(int=value)
