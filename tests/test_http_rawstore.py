"""The HTTP fetcher (against a loopback server) and the write-once raw file store."""

from __future__ import annotations

import hashlib
import http.server
import pathlib
import threading
from collections.abc import Iterator

import pytest

from canary.http import AccessRefused, Fetcher, FetchFailed
from canary.rawstore import RawStore

UA = "canary-personal-tool"


class Handler(http.server.BaseHTTPRequestHandler):
    requests: list[tuple[str, str | None]] = []
    location = ""

    def do_GET(self) -> None:  # noqa: N802
        type(self).requests.append((self.path, self.headers.get("User-Agent")))
        path = self.path.split("?")[0]
        if path == "/redirect":
            self.send_response(302)
            self.send_header("Location", type(self).location)
            self.send_header("Content-Length", "0")
            self.end_headers()
            return
        if path == "/badlength":
            self.send_response(200)
            self.send_header("Content-Length", "abc")
            self.end_headers()
            self.wfile.write(b"hello")
            return
        status = {"/ok": 200, "/401": 401, "/403": 403, "/451": 451, "/500": 500}.get(
            self.path.split("?")[0], 404
        )
        body = b"hello" if status == 200 else b"no"
        self.send_response(status)
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)

    def log_message(self, *args: object) -> None:
        pass


@pytest.fixture
def server(monkeypatch: pytest.MonkeyPatch) -> Iterator[str]:
    for name in (
        "http_proxy",
        "https_proxy",
        "HTTP_PROXY",
        "HTTPS_PROXY",
        "all_proxy",
        "ALL_PROXY",
    ):
        monkeypatch.delenv(name, raising=False)
    monkeypatch.setenv("no_proxy", "127.0.0.1")
    monkeypatch.setenv("NO_PROXY", "127.0.0.1")
    Handler.requests = []
    httpd = http.server.ThreadingHTTPServer(("127.0.0.1", 0), Handler)
    thread = threading.Thread(target=httpd.serve_forever, daemon=True)
    thread.start()
    try:
        yield f"http://127.0.0.1:{httpd.server_address[1]}"
    finally:
        httpd.shutdown()
        httpd.server_close()
        thread.join(timeout=5)


def test_get_returns_body_and_sends_the_literal_user_agent(server: str) -> None:
    assert Fetcher().get(f"{server}/ok") == b"hello"
    assert Handler.requests == [("/ok", UA)]


def test_get_sends_params_in_the_query_string(server: str) -> None:
    Fetcher().get(f"{server}/ok", params={"format": "json", "page": "2"})
    path = Handler.requests[0][0]
    assert "format=json" in path and "page=2" in path


@pytest.mark.parametrize("status", [401, 403, 451])
def test_refusal_statuses_raise_access_refused_with_one_request(server: str, status: int) -> None:
    with pytest.raises(AccessRefused) as caught:
        Fetcher().get(f"{server}/{status}")
    assert str(status) in str(caught.value)
    assert len(Handler.requests) == 1
    assert Handler.requests[0][1] == UA


def test_other_failures_raise_fetch_failed(server: str) -> None:
    with pytest.raises(FetchFailed):
        Fetcher().get(f"{server}/500")
    with pytest.raises(FetchFailed):
        Fetcher().get(f"{server}/missing")


# --- RawStore --------------------------------------------------------------


def test_put_lays_the_file_out_by_source_and_digest(tmp_path: pathlib.Path) -> None:
    data = b"a,b\n1,2\n"
    digest = hashlib.sha256(data).hexdigest()
    ref = RawStore(tmp_path).put("src-x", "data.csv", data)
    assert ref.sha256 == digest
    assert ref.size_bytes == len(data)
    expected = tmp_path / "src-x" / digest / "data.csv"
    assert pathlib.Path(ref.path) == expected
    assert expected.read_bytes() == data


def test_identical_put_returns_the_same_ref_and_leaves_the_file_untouched(
    tmp_path: pathlib.Path,
) -> None:
    store = RawStore(tmp_path)
    first = store.put("src-x", "data.csv", b"same")
    before = pathlib.Path(first.path).stat()
    second = store.put("src-x", "data.csv", b"same")
    after = pathlib.Path(second.path).stat()
    assert (second.path, second.sha256, second.size_bytes) == (
        first.path,
        first.sha256,
        first.size_bytes,
    )
    assert (before.st_ino, before.st_mtime_ns) == (after.st_ino, after.st_mtime_ns)
    assert len(list(pathlib.Path(first.path).parent.iterdir())) == 1


def test_different_content_under_one_name_is_kept_beside_the_first(tmp_path: pathlib.Path) -> None:
    store = RawStore(tmp_path)
    first = store.put("src-x", "data.csv", b"one")
    second = store.put("src-x", "data.csv", b"two")
    assert first.path != second.path
    assert pathlib.Path(first.path).read_bytes() == b"one"
    assert pathlib.Path(second.path).read_bytes() == b"two"


@pytest.mark.parametrize("name", ["a/b.csv", "../x.csv", "..", "x/../y.csv", "/abs.csv"])
def test_filename_with_separator_or_dotdot_is_refused_and_writes_nothing(
    tmp_path: pathlib.Path, name: str
) -> None:
    root = tmp_path / "raw"
    with pytest.raises(ValueError):
        RawStore(root).put("src-x", name, b"data")
    assert not root.exists() or not any(root.rglob("*.csv"))
    assert not (tmp_path / "x.csv").exists()


def test_default_root_comes_from_canary_raw_dir(
    tmp_path: pathlib.Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    monkeypatch.setenv("CANARY_RAW_DIR", str(tmp_path / "rawdir"))
    ref = RawStore().put("src-x", "d.txt", b"x")
    assert pathlib.Path(ref.path).is_relative_to(tmp_path / "rawdir")


# --- review fixes: only HTTP and HTTPS ---------------------------------------


def test_file_url_is_refused_without_reading_the_file(tmp_path: pathlib.Path) -> None:
    target = tmp_path / "secret.txt"
    target.write_text("secret")
    with pytest.raises(FetchFailed):
        Fetcher().get(target.as_uri())


def test_ftp_url_is_refused() -> None:
    with pytest.raises(FetchFailed):
        Fetcher().get("ftp://127.0.0.1:1/file.csv")


@pytest.mark.parametrize("scheme", ["file", "ftp"])
def test_redirect_to_a_non_http_scheme_is_refused(
    server: str, tmp_path: pathlib.Path, scheme: str
) -> None:
    target = tmp_path / "secret.txt"
    target.write_text("secret")
    Handler.location = target.as_uri() if scheme == "file" else "ftp://127.0.0.1:1/secret.txt"
    with pytest.raises(FetchFailed):
        Fetcher().get(f"{server}/redirect")
    assert [path for path, _ in Handler.requests] == ["/redirect"]


def test_malformed_content_length_is_fetch_failed_not_value_error(server: str) -> None:
    with pytest.raises(FetchFailed):
        Fetcher().get(f"{server}/badlength")
