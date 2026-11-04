# Contract: provenance spine

Spec: `docs/08` sections 1, 2 and 8, and `docs/10` Phase 0. This contract decides what the spec left
open, and it wins where they differ. Tests run on a real PostgreSQL 17 through the fixtures in
`tests/conftest.py`.

## Files

- `src/canary/ids.py`, `src/canary/schema.py` (SQLAlchemy Core metadata), `src/canary/provenance.py`
- `migrations/versions/0002_provenance.py`, with `down_revision = "0001"`
- `src/canary/cli.py`, gaining the commands below

## Identifiers

`ids.new_id() -> uuid.UUID` returns a version 7 UUID. Two calls in time order sort in time order
when the calls are at least a millisecond apart.

## Tables

Timestamps are `timestamptz`. All of them are required unless marked nullable.

- **pipeline_run**: `id` uuid primary key; `stage` text, checked against ingest, normalise, extract,
  support_check, lineage, event_assembly, indicator, baseline, change_detection, watch_rules,
  coverage, embed, translate, draft; `started_at`; `ended_at` nullable; `code_commit` text;
  `config_digest` text; nullable text `model_id`, `prompt_version`, `schema_version`,
  `indicator_catalog_version`, `rule_file_version`, `notes`; integers `input_count`, `output_count`,
  `error_count`, default 0.
- **source**: `id` text primary key, the registry id; `current_version` integer; `canary_use` text;
  `status` text; `record` jsonb. Updated only by a registry sync. Never deleted.
- **source_version**: `source_id` references source; `version` integer; `record` jsonb; `digest` text;
  `run_id` references pipeline_run; `recorded_at`. Primary key is (`source_id`, `version`).
- **source_health**: `id` uuid primary key; `source_id` references source; `checked_at`; `ok` boolean;
  nullable `latency_ms` integer, `items_seen` integer, `schema_digest` text, `message` text.
- **dataset_release**: `id` uuid primary key; `source_id` references source; `version_label` text;
  `released_at` nullable; `retrieved_at`; `file_refs` jsonb; `content_digest` text; `row_count` integer;
  `schema_digest` text; `licence_snapshot` text; `run_id` references pipeline_run. Unique on
  (`source_id`, `content_digest`). `content_digest` is an addition to `docs/08`: it is what makes a
  re-run idempotent.

## Write rules, enforced by database triggers

1. `source_version`, `source_health` and `dataset_release` refuse UPDATE and DELETE.
2. `pipeline_run` refuses DELETE. It allows one UPDATE only: from `ended_at` null to not null, changing
   nothing except `ended_at`, the three counts and `notes`. Any other UPDATE is refused.
3. `source` refuses DELETE and allows UPDATE.
4. A refusal raises a database error. TRUNCATE is refused on all five tables.

Each trigger line in the migration carries the suite's guard marker in a same-line comment, as
`~/.agents/AGENTS.md` describes under destructive code.

## provenance.py

Every function takes a SQLAlchemy `Session` first and does not commit; the caller owns the transaction.

- `start_run(session, stage, *, code_commit, config_digest, started_at=None, **versions) -> uuid.UUID`.
  `versions` accepts only the five nullable version-and-model fields, and `notes`; anything else raises
  `TypeError`. `started_at` defaults to now in UTC.
- `finish_run(session, run_id, *, input_count=0, output_count=0, error_count=0, notes=None, ended_at=None)`.
- `sync_registry(session, entries, *, run_id) -> SyncResult`, with `added`, `changed`, `unchanged` and
  `missing` as sorted lists of ids. The digest is SHA-256 of the entry's JSON with sorted keys and dates
  in ISO form. New id: a `source` row and version 1. Changed digest: a new version, and the `source` row
  updated. Same digest: nothing written. `missing`: ids in the table and not in `entries`, reported and
  left untouched. A second identical sync writes no rows.
- `record_health(session, source_id, *, ok, latency_ms=None, items_seen=None, schema_digest=None,
  message=None, checked_at=None) -> uuid.UUID`.
- `record_release(session, source_id, *, version_label, content_digest, row_count, schema_digest,
  licence_snapshot, file_refs, run_id, retrieved_at=None, released_at=None) -> tuple[uuid.UUID, bool]`.
  The boolean is true when a row was written. A repeated (`source_id`, `content_digest`) writes nothing
  and returns the existing id with false, even under a different `version_label` or `run_id`.
- `health_report(session, now=None) -> list[SourceHealth]`, sorted by id, one per `source` row, with fields
  `source_id`, `status`, `canary_use`, `last_ok_at` (the latest of ok health checks and release
  `retrieved_at`, or null), `last_failure_at` (latest failed check, or null), `expected_lag_days` (from
  `record`, or null) and `freshness`:
  - `never_fetched` when `last_ok_at` is null;
  - `unknown` when `last_ok_at` is set and `expected_lag_days` is null;
  - `stale` when the time since `last_ok_at` is more than `expected_lag_days` days;
  - `fresh` otherwise. Exactly `expected_lag_days` days is fresh.

## CLI

The database comes from `CANARY_DATABASE_URL`. When it is unset, a command that needs it prints a message
naming the variable to stderr and returns 2.

- `canary registry sync [--path DIR]`: validates, starts an `ingest` run, syncs, finishes the run and
  commits. Prints `added N, changed N, unchanged N, missing N`; returns 0. An invalid registry prints each
  problem to stderr, returns 1 and writes nothing.
- `canary health`: prints one line per source as `<id> <freshness> <last_ok_at or never>`; returns 0.
- `canary registry validate` and `main([])` keep their current behaviour.

`code_commit` for the sync run is the output of `git rev-parse HEAD`, or `unknown` when git fails.
`config_digest` is the SHA-256 of the sorted entry digests.

## Out of scope

Observations, indicators, adapters, `canary status`, a `document` table, database roles.
