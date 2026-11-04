# Contract: ingestion runner and dataset adapters

Spec: `docs/07` section 3, `docs/09` section 1, `docs/10` Phase 0. This contract decides what the spec left
open, and it wins where they differ. Formats below were read from the live sources on 2026-11-04 (note H-05).

## Files

`src/canary/http.py`, `src/canary/rawstore.py`, `src/canary/ingest.py`, `src/canary/geo.py`,
`src/canary/adapters/` (one module per family, plus `__init__.py` with `ADAPTERS`), `reference/country_aliases.csv`,
`migrations/versions/0004_place.py`, and additions to `schema.py`, `observations.py` (`table_counts`) and `cli.py`.

## Plumbing

- `http.Fetcher.get(url, *, params=None, headers=None, max_bytes=500_000_000, timeout_seconds=120) -> bytes`. Standard
  library only. It honours proxy variables and always sends `User-Agent: canary-personal-tool`. HTTP 401, 403 and 451
  raise `AccessRefused(url, status)`, with no retry and no change of client identity. Other failures raise `FetchFailed`.
- `rawstore.RawStore(root)`. `put(source_id, filename, data) -> RawRef`, with `path`, `sha256`, `size_bytes`. Files live at
  `<root>/<source_id>/<sha256>/<filename>`, are written through a temporary name and an atomic rename, and are never
  removed or overwritten. A `filename` containing a path separator or `..` raises `ValueError`. The default root is
  `CANARY_RAW_DIR`, else `~/.cache/canary/raw`.
- Manual sources read from `<CANARY_DROP_DIR or ~/.cache/canary/drop>/<source_id>/`. No matching file raises
  `ManualFileMissing`, whose message names that folder and the page to download from.

## Adapter interface

Each adapter has `source_id` and `config_digest()`, and these steps:
- `discover(fetcher) -> ReleaseRef`, with `version_label`, `urls` as a filename-to-URL mapping, `released_at` or null.
- `fetch(fetcher, ref, store) -> list[RawRef]`.
- `parse(refs, resolver) -> ParseResult`, with `indicators` (`IndicatorSpec` list), `rows` (`ObservationRow` list), `places`,
  `skipped` (a count), `unmapped` (a sorted list of source names with no `geo_ref`), and `schema_digest` (SHA-256 of
  the column names read).

`parse` is pure: no network and no database. A missing expected column raises `SchemaChanged`, naming the column. It
never yields a partial result for a changed file.

## Runner: `ingest.ingest(session, adapter, fetcher, store) -> IngestResult`

1. The source must exist in `source` with `canary_use` of open or display. Otherwise raise `NotPermitted`, before any fetch.
2. Start an `ingest` run with the code commit and `adapter.config_digest()`.
3. Discover and fetch. The content digest is SHA-256 of the sorted `<filename>:<sha256>` lines.
4. In a nested transaction: parse, record the release, sync indicators, write observations and upsert places.
5. Record health with `ok=True` and `items_seen` set to the parsed row count.
6. Finish the run with input and output counts.

A release already recorded for that digest writes no observations, and still records ok health and finishes its run.
On `AccessRefused`, `FetchFailed`, `ManualFileMissing` or `SchemaChanged`: the nested transaction rolls back, health is
recorded with `ok=False` and the message, the run finishes with `error_count=1`, and the exception is re-raised. The
caller commits, so the failure record survives. `IngestResult` has `source_id`, `version_label`, `new_release`,
`written`, `unchanged`, `skipped`, `unmapped`.

## Countries

- **place** table, migration 0004, down_revision "0003": `id` text primary key (ISO alpha-3); `iso2`; `name`;
  `continent`; `geonames_id` integer; nullable `wikidata_id`; `run_id` references pipeline_run. It refuses DELETE and
  TRUNCATE by trigger, as the spine's tables do. Upserts are allowed.
- `geo.CountryResolver(names, aliases)`, with `resolve(name) -> str | None`: exact match after case-folding and trimming,
  against place names and then `reference/country_aliases.csv` (`source_name,iso3,note`). No fuzzy matching. A name
  it cannot resolve stays unresolved and is never guessed. `geo.load_resolver(session)` builds it, and raises
  `SchemaChanged` with a message saying to ingest geonames first when `place` is empty.
- Where a row has no resolved country, it is left out and counted in `skipped`, and its source name goes in `unmapped`.
  Historical entities in V-Dem keep V-Dem's own `country_text_id`, which is already their `geo_ref`.

## Adapters

Indicator ids are the left-hand names below. Period means 1 January to 31 December for a year, and the first to the last
day for a month. Blank or `NA` values are left out of `rows` and not counted as skipped.

| Source | Discover and fetch | Parse |
|---|---|---|
| `vdem-country-year` | Label from `Version:` in `vdemdata/master/DESCRIPTION`; fetch `data/vdem.RData` and `data/codebook.RData` | Read with pyreadr, importing it inside the function. For each of `v2x_polyarchy`, `v2x_libdem`, `v2x_partipdem`, `v2x_delibdem`, `v2x_egaldem`, `v2x_jucon`, `v2xlg_legcon`, `v2x_freexp_altinf`, `v2x_frassoc_thick`, `v2xcl_rol`, `v2x_cspart`, `v2x_civlib`, `v2x_clphy`, `v2xel_frefair`, and `v2x_corr`: indicator `vdem-<column>`, `geo_ref` `country_text_id`, per year, `value_low` and `value_high` from `_codelow` and `_codehigh`. Direction is down, except `v2x_corr`, which is up. Name and definition come from the codebook file; a column missing there raises `SchemaChanged`. Keep the frame-to-row step in a function taking plain dicts, so it is testable without an R file. |
| `vdem-ert` | Label from `Version:` in `ERT/master/DESCRIPTION`; fetch `inst/ert.csv` | `ert-aut-ep` from `aut_ep` and `ert-dem-ep` from `dem_ep`, values 0 or 1, per `country_text_id` and `year`. Direction: up for `aut`, none for `dem`. |
| `ucdp-candidate` | From the downloads page, take the highest `GEDEvent_v<a>_01_<b>_<c>.csv`, else the highest `GEDEvent_v<a>_0_<n>.csv`; label is the file's version part | Per `country` and month of `date_start`: `ucdp-candidate-events` (count) and `ucdp-candidate-deaths` (sum of `best`, with sums of `low` and `high`). The bias note says events are preliminary and often carry `Check` statuses. |
| `ucdp-ged` | Highest `ged<nnn>-csv.zip` on that page | As above, from the zip's one CSV, as `ucdp-ged-events` and `ucdp-ged-deaths`. |
| `ucdp-prio-acd` | Highest `ucdp-prio-acd-<nnn>-csv.zip` on that page | Per country in `location` (split on `, `) and `year`: `acd-active-conflicts` (count of rows) and `acd-war-conflicts` (count with `intensity_level` 2, zero included). |
| `world-bank-indicators` | Label is `lastupdated` from the first series response. Fetch `/v2/country?format=json&per_page=400` and, for each series, `/v2/country/all/indicator/<code>?format=json&per_page=20000&date=1960:<this year>`, following `pages` | Series `FP.CPI.TOTL.ZG`, `NY.GDP.PCAP.KD.ZG`, `SL.UEM.TOTL.ZS`, `SP.POP.TOTL`: indicator `wb-<code>`, `geo_ref` `countryiso3code`, per `date`. Countries whose `region.value`, trimmed, is `Aggregates` are left out and counted in `skipped`, as are empty codes. Direction: up for inflation and unemployment, down for growth, none for population. |
| `our-world-in-data` | One class instance per allow-list. `SERIES` is the module's cleared list, and it is empty today. For each slug, fetch `<slug>.csv?useColumnShortNames=true` and `<slug>.metadata.json`. Label is the latest `lastUpdated`. With an empty list, `ingest` raises nothing and records no release | Columns `entity`, `code`, `year`, and one value column per metadata entry. Indicator `owid-<slug>-<column>`, `geo_ref` `code`; a blank code is skipped. |
| `ewp-sra` | Find `api/sra/download/csv/<nnnn>-sra` on `reports-and-downloads`, highest; label `<nnnn>-sra` | Find the column `risk_in_<y1>_<y2>`; none raises `SchemaChanged`. `ewp-sra-risk` is that value per `ISO3`, period 1 January `y1` to 31 December `y2`. `ewp-sra-rank` is `riskrank`, same period. Values unchanged. Direction: up for risk, none for rank. |
| `cline-coups` | Manual. Any `*.csv` in the drop folder; two or more raise `ManualFileMissing`. Label comes from the file name, for example `2.2.2`, else `unknown` | Columns `country`, `year`, `realized`, `attempt`, `conspiracy`, read as given. Per country and year with at least one row: `cline-realized`, `cline-attempts`, `cline-conspiracies`, each the sum of its flag. |
| `geonames` | Fetch `countryInfo.txt`; label is the file's SHA-256, first 12 characters | Lines not starting with `#`, tab-separated: ISO, ISO3, Country, Continent, geonameid by the `#ISO` header line. Yields `places` only. A changed header line raises `SchemaChanged`. |
| `wikidata` | SPARQL at `query.wikidata.org` for items with property P298, as CSV; label is the file's SHA-256, first 12 characters | For each alpha-3 code, the item with the smallest numeric Q id. Sets `place.wikidata_id` on existing places, adding none. |
| `natural-earth` | Fetch `https://naciscdn.org/naturalearth/50m/cultural/ne_50m_admin_0_countries.zip`; label is the file's SHA-256, first 12 characters | No rows. The file is kept for the Phase 2 map. |

Each spec's `reporting_bias_note` is one honest sentence, without invented figures. `ADAPTERS` maps source id to a factory.
Adapters use each indicator's `unit` and `cadence` as the source states them.

## CLI

- `canary ingest <source_id>`: returns 0 on success and prints
  `<id> <label> new|existing written=N unchanged=N skipped=N unmapped=N`. `AccessRefused`, `FetchFailed`,
  `ManualFileMissing`, `SchemaChanged` and `NotPermitted` print to stderr and return 1, keeping the failure record. An
  unknown source id returns 1. An unset `CANARY_DATABASE_URL` returns 2.
- `canary db start|stop|url`: the private development server in `canary.devdb`. `start` also creates a `canary` database
  if absent and migrates to head. `url` prints the URL.

## Tests

Fixture-based, never live: small files under `tests/fixtures/<source_id>/`, using the real column headers and invented
rows, plus a recording fake fetcher. Each adapter also has a changed-schema fixture that must produce failed health and no
observations. A reproducibility test ingests the same fixtures into two databases and compares `observation_digest`.

## Out of scope

Live downloads in the test suite, scheduling, GDELT, OONI, news feeds, the indicator catalog files, computing baselines.

## Settled after test authoring (2026-11-04)

- All five exceptions live in `src/canary/errors.py`. `FetchFailed` takes one message argument; `AccessRefused`
  takes `(url, status)`.
- `CountryResolver(names, aliases)` takes two dicts: name to alpha-3, and source name to alpha-3.
- The V-Dem module exposes `rows_from_records(records, codebook) -> ParseResult`, where `codebook[column]` is
  `{"name", "definition"}`.
- `our-world-in-data` takes its allow-list as the constructor's one argument. Metadata is read as
  `{"columns": {column: {titleShort, descriptionShort, unit, lastUpdated}}}`.
- The live Early Warning column is `risk_in_2025_26`, so a two-digit second year means the same century. A
  column with one year, like `risk_in_2025`, never matches.
- The Wikidata query selects `?item ?code`, so its CSV columns are `item,code`.
- `ReleaseRef.urls` keys are file basenames. World Bank paging adds `page=<n>` to the query.
- `skipped` counts source rows, not country parts. The runner calls `load_resolver` for adapters that need it,
  and geonames does not. Geonames stores `continent` as the raw code.
