"""Write-once storage for downloaded files, laid out by source and content digest."""

from __future__ import annotations

import hashlib
import os
import pathlib
import tempfile
from dataclasses import dataclass


@dataclass(frozen=True)
class RawRef:
    path: str
    sha256: str
    size_bytes: int


def _default_root() -> pathlib.Path:
    configured = os.environ.get("CANARY_RAW_DIR")
    return pathlib.Path(configured) if configured else pathlib.Path.home() / ".cache/canary/raw"


def _check_name(name: str) -> None:
    if not name or name == "." or ".." in name or "/" in name or "\\" in name:
        raise ValueError(f"unsafe file name: {name!r}")


class RawStore:
    def __init__(self, root: str | os.PathLike[str] | None = None) -> None:
        self.root = pathlib.Path(root) if root is not None else _default_root()

    def put(self, source_id: str, filename: str, data: bytes) -> RawRef:
        _check_name(source_id)
        _check_name(filename)
        digest = hashlib.sha256(data).hexdigest()
        folder = self.root / source_id / digest
        target = folder / filename
        ref = RawRef(path=str(target), sha256=digest, size_bytes=len(data))
        if target.exists():
            return ref
        folder.mkdir(parents=True, exist_ok=True)
        handle, temporary = tempfile.mkstemp(dir=folder, prefix=".incoming-")
        with os.fdopen(handle, "wb") as stream:
            stream.write(data)
            stream.flush()
            os.fsync(stream.fileno())
        os.rename(temporary, target)
        return ref
