"""The failures the ingestion runner and the CLI know how to report."""

from __future__ import annotations


class AccessRefused(Exception):
    """The source said no (401, 403 or 451). It is never retried."""

    def __init__(self, url: str, status: int) -> None:
        super().__init__(f"access refused with HTTP {status}: {url}")
        self.url = url
        self.status = status


class FetchFailed(Exception):
    """The fetch failed for any reason other than a refusal."""


class ManualFileMissing(Exception):
    """A hand-downloaded file is absent from the drop folder, or ambiguous."""


class SchemaChanged(Exception):
    """A source no longer has the shape an adapter expects."""


class NotPermitted(Exception):
    """The registry does not clear this source for ingestion."""
