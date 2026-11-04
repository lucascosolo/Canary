"""The one HTTP client. Standard library only, one identity, and no retries."""

from __future__ import annotations

import urllib.error
import urllib.parse
import urllib.request
from collections.abc import Mapping
from http.client import HTTPException

from canary.errors import AccessRefused, FetchFailed

USER_AGENT = "canary-personal-tool"
REFUSALS = (401, 403, 451)
CHUNK_BYTES = 1 << 20


def _opener() -> urllib.request.OpenerDirector:
    """HTTP and HTTPS only: with no file or FTP handler, those schemes reach UnknownHandler."""
    proxies = {
        scheme: proxy
        for scheme, proxy in urllib.request.getproxies().items()
        if scheme in ("http", "https")
    }
    opener = urllib.request.OpenerDirector()
    for handler in (
        urllib.request.ProxyHandler(proxies),
        urllib.request.UnknownHandler(),
        urllib.request.HTTPHandler(),
        urllib.request.HTTPSHandler(),
        urllib.request.HTTPRedirectHandler(),
        urllib.request.HTTPDefaultErrorHandler(),
        urllib.request.HTTPErrorProcessor(),
    ):
        opener.add_handler(handler)
    return opener


class Fetcher:
    def __init__(self) -> None:
        self._opener = _opener()

    def get(
        self,
        url: str,
        *,
        params: Mapping[str, str] | None = None,
        headers: Mapping[str, str] | None = None,
        max_bytes: int = 500_000_000,
        timeout_seconds: float = 120,
    ) -> bytes:
        full = url
        if params:
            full += ("&" if "?" in url else "?") + urllib.parse.urlencode(params)
        request = urllib.request.Request(full)
        for name, value in (headers or {}).items():
            request.add_header(name, value)
        request.add_header("User-Agent", USER_AGENT)
        try:
            with self._opener.open(request, timeout=timeout_seconds) as response:
                return _read(response, full, max_bytes)
        except urllib.error.HTTPError as exc:
            exc.close()
            if exc.code in REFUSALS:
                raise AccessRefused(full, exc.code) from exc
            raise FetchFailed(f"HTTP {exc.code}: {full}") from exc
        except (OSError, HTTPException) as exc:
            raise FetchFailed(f"{exc}: {full}") from exc


def _read(response, url: str, max_bytes: int) -> bytes:
    chunks: list[bytes] = []
    total = 0
    while chunk := response.read(CHUNK_BYTES):
        total += len(chunk)
        if total > max_bytes:
            raise FetchFailed(f"larger than {max_bytes} bytes: {url}")
        chunks.append(chunk)
    declared = response.headers.get("Content-Length")
    if declared is not None and (not declared.isdecimal() or int(declared) != total):
        raise FetchFailed(f"got {total} bytes but Content-Length says {declared!r}: {url}")
    return b"".join(chunks)
