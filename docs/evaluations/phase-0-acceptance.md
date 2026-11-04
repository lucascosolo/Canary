# Phase 0 acceptance evidence, 2026-11-04

Live ingest on this PC against a private PostgreSQL 17.11. Criteria are from `docs/10`, Phase 0.

| Criterion | Result |
|---|---|
| Every adapter ingests its current release | Met for 10 sources. `cline-coups` waits for a hand-downloaded file. `our-world-in-data` has no cleared series, by decision. |
| A re-run adds no observation rows | Met: every source reports `written=0` on the third pass below, and digests match across passes. |
| `canary health` reports freshness | Met; output below predates the staleness allowances, so it shows `unknown` where one was unset. |
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
=== second pass, aliases added ===
geonames 79f8f59ea01c existing written=0 unchanged=0 skipped=0 unmapped=0
wikidata 926cf5522fe7 existing written=0 unchanged=0 skipped=0 unmapped=0
natural-earth 5fed43337358 existing written=0 unchanged=0 skipped=0 unmapped=0
vdem-ert 16.0 existing written=0 unchanged=39714 skipped=0 unmapped=0
ewp-sra 2026-sra new written=336 unchanged=0 skipped=0 unmapped=0
ucdp-prio-acd 261 existing written=612 unchanged=3552 skipped=17 unmapped=3
ucdp-candidate 26_01_26_09 existing written=78 unchanged=820 skipped=0 unmapped=0
ucdp-ged 261 existing written=3458 unchanged=27224 skipped=0 unmapped=0
world-bank-indicators 2026-10-08 existing written=0 unchanged=41382 skipped=12936 unmapped=5
vdem-country-year 16.0 existing written=0 unchanged=387947 skipped=0 unmapped=0
our-world-in-data none existing written=0 unchanged=0 skipped=0 unmapped=0
=== third pass, expect written=0 ===
geonames 79f8f59ea01c existing written=0 unchanged=0 skipped=0 unmapped=0
wikidata 926cf5522fe7 existing written=0 unchanged=0 skipped=0 unmapped=0
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
dataset_release 10
indicator 29
indicator_version 29
observation 505123
pipeline_run 36
place 252
source 19
source_health 34
source_version 19
=== health ===
cline-coups never_fetched never
cloudflare-radar never_fetched never
ewp-sra unknown 2026-11-04T20:22:39.377874+00:00
gdelt-doc never_fetched never
geonames unknown 2026-11-04T20:22:35.192337+00:00
global-legal-monitor never_fetched never
internet-archive never_fetched never
iso-3166 never_fetched never
keepiton never_fetched never
natural-earth unknown 2026-11-04T20:22:36.516732+00:00
ooni never_fetched never
our-world-in-data unknown 2026-11-04T20:23:12.885602+00:00
ucdp-candidate fresh 2026-11-04T20:22:46.008901+00:00
ucdp-ged unknown 2026-11-04T20:22:56.906717+00:00
ucdp-prio-acd unknown 2026-11-04T20:22:41.530139+00:00
vdem-country-year unknown 2026-11-04T20:23:12.347680+00:00
vdem-ert unknown 2026-11-04T20:22:38.330890+00:00
wikidata unknown 2026-11-04T20:22:35.802976+00:00
world-bank-indicators unknown 2026-11-04T20:23:01.073890+00:00
unmapped: Bosnia-Herzegovina; Cambodia (Kampuchea); Congo; DR Congo (Zaire); Hyderabad; Madagascar (Malagasy); Myanmar (Burma); Netherlands; Russia (Soviet Union); Serbia (Yugoslavia); South Vietnam; South Yemen; United States of America; Vietnam (North Vietnam); Yemen (North Yemen); Zimbabwe (Rhodesia)
unmapped: Bosnia-Herzegovina; Cambodia (Kampuchea); Congo; DR Congo (Zaire); Kingdom of eSwatini (Swaziland); Madagascar (Malagasy); Myanmar (Burma); Netherlands; Russia (Soviet Union); Serbia (Yugoslavia); United States of America; Yemen (North Yemen); Zimbabwe (Rhodesia)
unmapped: DR Congo (Zaire); Myanmar (Burma); Russia (Soviet Union); United States of America; Yemen (North Yemen)
unmapped: High income; Low income; Lower middle income; Not classified; Upper middle income
unmapped: Hyderabad; South Vietnam; South Yemen
```
