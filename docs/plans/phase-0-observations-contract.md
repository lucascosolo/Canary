# Contract: observations with vintages

Spec: `docs/08` sections 4 and 8, `docs/09` sections 1 and 5. This contract decides what the spec left
open, and it wins where they differ. It builds on `docs/plans/phase-0-spine-contract.md`.

## Files

- `src/canary/observations.py`; `src/canary/schema.py` gains the new tables
- `migrations/versions/0003_observations.py`, with `down_revision = "0002"`
- `src/canary/cli.py` gains `canary status`

## Tables

- **indicator**: `id` text primary key; `current_version` integer; `source_id` references source; `record`
  jsonb. Never deleted; updated only by `sync_indicator`.
- **indicator_version**: `indicator_id` references indicator; `version` integer; `record` jsonb; `digest`
  text; `recorded_at`. Primary key is (`indicator_id`, `version`). Append-only.
- **observation**: `id` uuid; `indicator_id` references indicator; `geo_ref` text; `period_start` date;
  `period_end` date; `value` double precision, required; nullable `value_low`, `value_high`;
  `vintage_release_id` references dataset_release; `retrieved_at`; `run_id` references pipeline_run.
  Primary key is (`id`, `retrieved_at`). Range-partitioned by month of `retrieved_at`. Check:
  `period_end >= period_start`. Index on (`indicator_id`, `geo_ref`, `period_start`, `retrieved_at`).
- **baseline**: `id` uuid primary key; `indicator_id` references indicator; `geo_ref` text; `horizon` text,
  checked against 12m, 5y, full; `computed_at`; `stats` jsonb; `method_version` text; `run_id` references
  pipeline_run. Computing baselines is Phase 2. This phase creates the table only.

## Write rules

`indicator_version`, `observation` and `baseline` refuse UPDATE, DELETE and TRUNCATE, by the same kind of
trigger as the spine. `indicator` refuses DELETE and TRUNCATE. A partition inherits the row rules and gets
its own TRUNCATE refusal when created, because statement triggers do not reach partitions. Truncating a
single partition directly must be refused.

## observations.py

Functions take a `Session` first and do not commit.

- `IndicatorSpec`: frozen dataclass with `id`, `source_id`, `name`, `definition`, `domain`, `unit`, `cadence`,
  `deterioration_direction` (up, down, none; anything else raises `ValueError`), `reporting_bias_note`.
- `sync_indicator(session, spec) -> int`: returns the current version. New id: version 1. Changed content:
  a new version. Same content: writes nothing.
- `ObservationRow`: frozen dataclass with `indicator_id`, `geo_ref`, `period_start`, `period_end`, `value`,
  `value_low=None`, `value_high=None`.
- `write_observations(session, release_id, run_id, rows) -> WriteResult`, with `written` and `unchanged`
  counts. `retrieved_at` is taken from the release, so every row of a vintage shares it. The key is
  (`indicator_id`, `geo_ref`, `period_start`, `period_end`). A row is written when the key is new, or when
  `value`, `value_low` or `value_high` differs from the latest vintage of that key. Otherwise it is counted
  as unchanged. Two rows with one key in one call raise `ValueError` and write nothing. NaN or infinite
  values raise `ValueError` and write nothing. A value that disappears from a later release keeps its
  last vintage. The needed monthly partition is created on demand. It must not issue one query per row.
- `observations_as_of(session, indicator_id, as_of, *, geo_ref=None) -> list[StoredObservation]`: for each key,
  the row with the latest `retrieved_at` at or before `as_of`, sorted by `geo_ref`, then `period_start`, then
  `period_end`. `StoredObservation` has the `ObservationRow` fields plus `vintage_release_id`, `retrieved_at`
  and `run_id`. Keys first seen after `as_of` are absent.
- `observation_digest(session, source_id, as_of=None) -> str`: SHA-256 over the as-of rows of every indicator
  of the source, ordered, using the indicator id, key and values only. Identifiers, run ids and timestamps
  do not affect it. Two databases loaded from the same inputs must give the same digest; this is the
  reproducibility check. Floats are rendered with `repr`.
- `table_counts(session) -> dict[str, int]`: row counts for pipeline_run, source, source_version, source_health,
  dataset_release, indicator, indicator_version, observation and baseline.

## CLI

`canary status` prints one line per table as `<table> <count>`, sorted by table name, and returns 0. It uses
the spine's rule for an unset `CANARY_DATABASE_URL`.

## Out of scope

Adapters, computing baselines, signals, the coverage index, indicator catalog files.

## Settled after test authoring (2026-11-04)

- An invalid `deterioration_direction` raises `ValueError` when `IndicatorSpec` is constructed.
- In `observation_digest`, a null `value_low` or `value_high` renders as the text `null`.
- An unknown `indicator_id` surfaces as the database's foreign-key error; `write_observations` does not
  check it first.
- Partition names are `observation_YYYY_MM`, and a partition refuses UPDATE and DELETE when addressed
  directly.
