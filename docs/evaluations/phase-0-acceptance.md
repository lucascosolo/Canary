# Phase 0 acceptance evidence, 2026-11-04

Live ingest on this PC against a private PostgreSQL 17.11, on a database rebuilt from empty after the review fixes in `docs/plans/phase-0-review-fixes.md`. Criteria are from `docs/10`, Phase 0.

| Criterion | Result |
|---|---|
| Every adapter ingests its current release | Met for 10 sources. `cline-coups` waits for a hand-downloaded file. `our-world-in-data` has no cleared series, by decision. |
| A re-run adds no observation rows | Met: every source reports `written=0` on the second pass below, and digests match across passes. Wikidata shows a false new release there, because its query had no order; that was then fixed, and three further live pulls gave one digest. |
| `canary health` reports freshness | Met; output below. `our-world-in-data` shows `unknown` because it has no cleared series. |
| Reproducibility test passes | Met on fixtures across two databases; the live digests also match across passes. |
| `canary status` prints counts per table | Met; output below. |
| Every observation traces to a release and a run | Met: zero rows without both. |
| Tests pass with a JUnit report | Met: `reports/junit.xml` from `uv run pytest`. |

## Separate check against the raw files

A script separate from the adapters re-read the stored raw files. Note that it uses the same country names and
aliases, so it checks arithmetic and loading, not the choice of alias.

## Differences from the `docs/10` plan

- PostgreSQL runs from PGDG binaries, not Docker, because the agent sandbox refuses the Docker socket. `compose.yaml` remains.
- FastAPI and Procrastinate are not installed yet, because nothing in this phase uses them. They arrive with Phases 1 and 2.
- V-Dem comes from GitHub, not the website form (`DECISIONS.md`).
- The Wikidata seed is an identifier per country on `place`. The actor alias table arrives in Phase 1 with claims.
- Natural Earth is stored but not parsed. The Phase 2 map uses it.
- `reference/country_aliases.csv` adopts UCDP's successor conventions, for example Soviet-era rows under Russia.

## Known limits

- Hyderabad, South Vietnam and South Yemen stay unmapped in the armed-conflict data: 17 rows are left out on purpose.
- UCDP Candidate events are preliminary. Many carry `Check` statuses.
- V-Dem and UCDP GED each peak above 2 GB while parsing, so they run on this PC, not the utility VPS.
- As-of queries cannot reach before the first retrieval, 2026-11-04. Phase 4 backtests must design for that.
- World Bank series are stored under the catalog's CC BY default, with per-series exceptions not checked one by one.

## Run output

```
=== first pass on an empty database ===
geonames 79f8f59ea01c new written=0 unchanged=0 skipped=0 unmapped=0
wikidata 926cf5522fe7 new written=0 unchanged=0 skipped=0 unmapped=0
natural-earth 5fed43337358 new written=0 unchanged=0 skipped=0 unmapped=0
vdem-ert 16.0 new written=39714 unchanged=0 skipped=0 unmapped=0
ewp-sra 2026-sra new written=336 unchanged=0 skipped=0 unmapped=0
ucdp-prio-acd 261 new written=4164 unchanged=0 skipped=17 unmapped=3
ucdp-candidate 26_01_26_09 new written=898 unchanged=0 skipped=0 unmapped=0
ucdp-ged 261 new written=30682 unchanged=0 skipped=0 unmapped=0
world-bank-indicators 2026-10-08 new written=41382 unchanged=0 skipped=12936 unmapped=5
vdem-country-year 16.0 new written=387947 unchanged=0 skipped=0 unmapped=0
our-world-in-data none existing written=0 unchanged=0 skipped=0 unmapped=0
=== second pass, expect written=0 ===
geonames 79f8f59ea01c existing written=0 unchanged=0 skipped=0 unmapped=0
wikidata a7d9d9b784b2 new written=0 unchanged=0 skipped=0 unmapped=0
natural-earth 5fed43337358 existing written=0 unchanged=0 skipped=0 unmapped=0
vdem-ert 16.0 existing written=0 unchanged=39714 skipped=0 unmapped=0
ewp-sra 2026-sra existing written=0 unchanged=336 skipped=0 unmapped=0
ucdp-prio-acd 261 existing written=0 unchanged=4164 skipped=17 unmapped=3
ucdp-candidate 26_01_26_09 existing written=0 unchanged=898 skipped=0 unmapped=0
ucdp-ged 261 existing written=0 unchanged=30682 skipped=0 unmapped=0
world-bank-indicators 2026-10-08 existing written=0 unchanged=41382 skipped=12936 unmapped=5
vdem-country-year 16.0 existing written=0 unchanged=387947 skipped=0 unmapped=0
our-world-in-data none existing written=0 unchanged=0 skipped=0 unmapped=0
digests identical across passes
V-Dem: 600 sampled rows, 0 differences; rows in file with a value equal rows stored
UCDP GED: 417968 source rows, 0 unmapped, 15341 country-months computed separately, 0 differences
  total deaths (best): source-mapped 4257891 stored 4257891
World Bank inflation: 1 files, 9151 rows compared, 0 differences, 9151 stored
Early Warning: rows 168 stored 168 differences 0
  top ranked: ['MMR', 'TCD', 'SDN']
Trace: observations without a release or run: 0
Open runs: 0
Partitions: ['observation_2026_11']
Places with Wikidata ids: (251, 252)
=== status ===
baseline 0
dataset_release 11
indicator 29
indicator_version 29
observation 505123
pipeline_run 23
place 252
place_version 503
source 19
source_health 22
source_version 19
=== health ===
cline-coups never_fetched never
cloudflare-radar never_fetched never
ewp-sra fresh 2026-11-04T20:40:14.572251+00:00
gdelt-doc never_fetched never
geonames fresh 2026-11-04T20:40:09.582323+00:00
global-legal-monitor never_fetched never
internet-archive never_fetched never
iso-3166 never_fetched never
keepiton never_fetched never
natural-earth fresh 2026-11-04T20:40:11.176733+00:00
ooni never_fetched never
our-world-in-data unknown 2026-11-04T20:40:48.271469+00:00
ucdp-candidate fresh 2026-11-04T20:40:21.386775+00:00
ucdp-ged fresh 2026-11-04T20:40:32.710763+00:00
ucdp-prio-acd fresh 2026-11-04T20:40:16.857846+00:00
vdem-country-year fresh 2026-11-04T20:40:47.741166+00:00
vdem-ert fresh 2026-11-04T20:40:13.175724+00:00
wikidata fresh 2026-11-04T20:40:10.360833+00:00
world-bank-indicators fresh 2026-11-04T20:40:36.859719+00:00
place versions (2, 503)
file_refs sample [{'url': 'https://ucdp.uu.se/downloads/ged/ged261-csv.zip', 'sha256': '8c941d84954e555ee2e54f40fa04d9203bf1e2f962203d0a9930966c4947c667', 'filename': 'ged261-csv.zip', 'size_bytes': 39122522}]
health messages [('world-bank-indicators', 'unmapped: 5'), ('ucdp-prio-acd', 'unmapped: 3')]
```
