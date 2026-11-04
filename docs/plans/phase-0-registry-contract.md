# Contract: source registry loader

Spec: `docs/03` section 7 (fields) and section 8 (policy). This contract decides what the spec left
open, and it wins where they differ.

## Files

- `registry/<id>.yaml`: one source per file; the file name without extension equals `id`.
- `src/canary/registry.py`: the model and loader. No database access and no network.
- `src/canary/cli.py`: gains `canary registry validate [--path DIR]`, default `registry`.

## API

- `SourceEntry`: a frozen Pydantic model that rejects unknown keys.
- `load_registry(directory: pathlib.Path, today: datetime.date | None = None) -> list[SourceEntry]`:
  returns entries sorted by `id`. `today` defaults to the current date and exists for testing.
- `RegistryError(Exception)`: has `problems: list[str]`. Every problem names the file. The loader
  reads every file and reports all problems together, not only the first.
- A missing directory raises `RegistryError`. An empty directory returns `[]`. Only `*.yaml` is read.

## Fields

Required unless marked optional. Optional fields default to `None`.

| Field | Rule |
|---|---|
| `id` | lowercase kebab-case, `^[a-z0-9][a-z0-9-]*$`, equals the file name |
| `name`, `organisation`, `homepage` | non-empty strings; `homepage` starts with `https://` or `http://` |
| `type` | index, event_dataset, api, rss, document_feed, catalog, reference, model_output |
| `domains` | non-empty list of: institutions, elections, legislation, conflict, rights, information, economy, humanitarian, reference |
| `countries` | the string `global`, or a non-empty list of `^[A-Z]{3}$` codes |
| `languages` | non-empty list of `^[a-z]{2,3}$` codes |
| `declared_cadence` | non-empty string |
| `expected_lag_days` | integer, zero or more; optional |
| `revision_policy` | none, silent, announced |
| `access_method` | non-empty string |
| `endpoint` | string; optional |
| `auth` | none, key, token_by_request, account, credentials_by_request |
| `rate_limit_text` | string; optional |
| `adapter` | string; optional |
| `licence_id`, `terms_url` | strings; optional only when `canary_use` is `unverified` |
| `terms_verified_on` | date, not after `today`; optional only when `canary_use` is `unverified` |
| `canary_use` | open, display, links, permission, excluded, unverified |
| `attribution_text` | non-empty string; required when `canary_use` is open or display, else optional |
| `redistribution_notes` | string; optional |
| `source_class` | official_government, intergovernmental, ngo_advocacy, ngo_documentation, academic, media_wire, media_national, media_local, state_media, platform, model_output |
| `state_control_class`, `funding_notes`, `quality_notes` | strings; optional |
| `status` | lead, evaluated, integrated, degraded, retired |
| `evaluated_on`, `integrated_on`, `retired_on` | dates; optional |
| `retired_reason` | string; optional |

## Policy invariants (each one is a validation error)

1. `status: integrated` requires `auth: none`, `canary_use` of open or display, a non-empty
   `adapter`, and `integrated_on`.
2. `status: retired` requires `retired_on` and `retired_reason`.
3. `status: evaluated` requires `evaluated_on`.
4. YAML that does not parse, or that is not a mapping, is a problem naming the file and does not
   stop the other files being read.

## CLI

`canary registry validate` prints `N sources valid` to stdout and returns 0. On `RegistryError` it
prints each problem on its own line to stderr and returns 1.

## Settled after test authoring (2026-11-04)

- The success line is literally `N sources valid`, including `1 sources valid`.
- A missing directory reaches the CLI as `RegistryError`, so it returns 1, for the default path too.
- An `id` that fails the pattern is a problem; a file-name mismatch may be reported beside it.
- Optional string fields may be empty unless the table says non-empty.
