# Phase 0 security review, 2026-11-04

The built-in review tool needs a branch diff against `origin/HEAD`, which this repository does not have, so the orchestrating session
read the code that handles untrusted input by hand: `http.py`, `rawstore.py`, link discovery and archive reading in `adapters/base.py`,
and SQL construction in `observations.py`, `geo.py` and `devdb.py`. This is one reader's pass, not a tool's output.

Fixed under `docs/plans/phase-0-review-fixes.md`:

- `urllib` opens `file://` and `ftp://`, and link discovery checked only a URL's path. A tampered downloads page could point an
  adapter at a local file, which would then be stored and parsed, or at another host.
- A zip archive was read whole with no size limit.
- A malformed `Content-Length` raised an unrecorded error.

Checked and acceptable:

- Raw file names are checked for separators and `..`, and files are written once by digest.
- Partition names are built only from a timestamp; database names are checked before use; values go through bound parameters.
- The development server uses `trust` authentication on loopback only, on a single-user PC. It must never be used on a server.
- `pyreadr` parses V-Dem's file in native code. The source is V-Dem's own repository on HTTPS, the dependency is locked, and the
  file's digest is recorded, but the file comes from a moving branch. It runs on this PC only.
- Source names are stored as plain text in run notes. Phase 2 templates must escape them, which Jinja2 does when autoescape is on.
