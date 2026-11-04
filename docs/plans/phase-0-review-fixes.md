# Contract: fixes from the Phase 0 reviews, 2026-11-04

An independent architecture review and a manual security review of the Phase 0 code found the items below. This
contract wins over the three earlier ones where they differ. Nothing has been deployed and the development database
is rebuilt from the raw files, so migrations 0003 and 0004 are edited in place rather than followed by a new one.

## Time: a row's `retrieved_at` is when Canary came to hold that value

Reviewers found three blocking faults with one cause: a re-parse wrote rows under the old release's `retrieved_at`, so an
as-of query for date D changed after D, and a source rolling back from B to A could not be told apart from A.

- `write_observations(session, release_id, run_id, rows, *, at=None)`. `retrieved_at` and the partition come from `at`, else
  from the release as today.
- The runner passes `at` equal to the run's `started_at` when the release was already known. For a new release it passes
  nothing, so rows share the release's `retrieved_at`.
- Comparison stays against the newest vintage of each key. The newest vintage is ordered by `retrieved_at` descending, then
  `id` descending, in both the latest-values and the as-of queries.
- Consequences to pin in tests:
  1. A country newly mapped on a re-parse is absent from an as-of query before the re-parse and present after it.
  2. An alias that maps a second name onto an existing country code writes a new vintage for the changed months, and the
     as-of query before the re-parse still returns the old sums.
  3. Releases A, B, A: the third ingest writes the rows that differ from B, under A's release id, stamped with that run's
     time. A fourth ingest writes nothing. As-of queries between them return A, then B, then A.
  4. Two rows of one key with the same `retrieved_at` resolve to the larger `id`.

The reviewer proposed filtering as-of queries on the run's `started_at`. This is rejected as a second clock for the same
fact. When a source published a value stays available through `vintage_release_id`.

## Tracing

- **place_version** (in migration 0004): `place_id` references place; `version` integer; `record` jsonb; `digest` text;
  `run_id` references pipeline_run; `recorded_at`. Primary key (`place_id`, `version`). It refuses UPDATE, DELETE and
  TRUNCATE. `place` gains `current_version` integer.
- A GeoNames ingest or a Wikidata link writes a `place_version` and updates `place` only when the record changed. Otherwise
  it writes nothing, so a poll causes no churn. `place.run_id` is the run of the current version. A Wikidata link adds
  `wikidata_id` to the record and leaves the other fields as they are. `table_counts` gains `place_version`.
- **indicator_version** gains `run_id`, required, referencing pipeline_run. `sync_indicator(session, spec, *, run_id)`.
- `geo.resolver_digest(session) -> str`: SHA-256 over sorted place names with their ids and the alias file's rows. It never
  raises, including on an empty table. A run's `config_digest` is SHA-256 of `adapter.config_digest()` plus this digest
  for adapters with `needs_resolver`, and `adapter.config_digest()` unchanged for others.
- A successful ingest with unmapped names records health `message` as `unmapped: <count>`, and `ok` stays true.
- `dataset_release.file_refs` entries gain `url`, taken from `ReleaseRef.urls`. Release rows cannot be updated later.

## Security

- `Fetcher` only speaks HTTP and HTTPS. It uses an explicit opener with proxy, HTTP, HTTPS, redirect and error handlers, with no
  file or FTP handler. A `file://` or `ftp://` URL raises `FetchFailed` without touching the disk, and so does a redirect to one.
- `page_link` and `highest_link` accept a link only when its scheme is `https` or `http` and its host equals the page's host. A
  matching link on another host, or a `file://` link, is ignored.
- A malformed `Content-Length` raises `FetchFailed`, not `ValueError`.
- `only_csv_in_zip` refuses an archive member whose declared size is over 2 GB, with `SchemaChanged`, before reading it.

## Recorded for later, not changed now

Each is an accepted gap with a named phase, listed in `docs/plans/phase-0.md`: retraction markers, because a nullable `value`
is a cheap later change; merging editorial indicator fields, Phase 2; a response object from `Fetcher` and a feed runner that commits
its run first, Phase 1; the `document` schema, Phase 1; a partition job run by the owning role, packaging `reference/` in the
wheel, a build-stamped commit, adapter `health()` probes and schedules, and skipping a re-parse when files and config are
unchanged, all Phase 2; loading older releases for honest backtests, Phase 4.
