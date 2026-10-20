# 07. Technical architecture

## 1. Shape of the system

A modular monolith around one PostgreSQL database: ingestion adapters write immutable raw
documents and observations; a processing pipeline derives claims, lineages, events, indicators
and signals, each step recorded as a run with its code, config, model and prompt versions; an
operator workspace turns flags into assessments; a public web application renders the three
layers. One codebase, one database, one job queue, deployable on one small server, with the
seams (adapters, pipeline stages, storage interfaces) placed where a later split would go. No
message broker, no search cluster, no graph database, no microservices until a measured limit
forces one (F-01).

## 2. Stack, with the alternatives considered

**Backend language: Python 3.13.** Alternatives: TypeScript (Node), Elixir (Phoenix LiveView),
Go. Python wins on the only axis that is hard to substitute: the NLP and statistics ecosystem
(spaCy, GLiNER, sentence-transformers, datasketch, ruptures, statsmodels, PyMC, geopandas,
mordecai3, trafilatura; versions current as of 2026-10-20 in note F-02), plus the official
Anthropic SDK. Elixir would give the best real-time dashboard and job story (Oban, Broadway) but
would put every NLP step behind a port to Python; TypeScript would split the pipeline across two
runtimes for no gain; Go has no NLP stack. Pinned to 3.13 rather than 3.14 or the two-week-old
3.15 because `ruptures` excludes 3.14+ and a public service should not ride a fresh runtime
(F-02).

**Web and API: FastAPI (0.153) on uvicorn, Pydantic 2, SQLAlchemy 2.1 with Alembic.** All MIT or
BSD, all current (F-02). Django was the alternative: its admin would give the operator workspace
for free, but Canary's operator screens are domain-specific (evidence records, comparisons) and
FastAPI's typed request models double as the public API contract.

**Jobs and scheduling: Procrastinate (3.10, MIT) on Postgres**, using `SKIP LOCKED`, with
periodic tasks for polling. Alternatives: Celery or Dramatiq (need Redis or RabbitMQ, which is a
second stateful system to run and back up), PGQueuer, pgmq. Procrastinate keeps the queue in the
same database as the data it processes, so a job and its output commit together (F-01).

**Database: PostgreSQL 17** (the version already on the utility VPS, supported to 2029; F-01)
with pg_trgm and the built-in text search with per-language configurations. Partitioned tables
with BRIN indexes for observations and documents by month. Not used (lighter-stack decision of
2026-10-20, 13:11 CDT): pgvector and any embedding index (duplicates are found by MinHash, search
by Postgres full text), PostGIS (places resolve to ISO country and GeoNames admin-1 identifiers in
Python; the map is static SVG), TimescaleDB, ParadeDB pg_search, Apache AGE, OpenSearch. Each is a
documented upgrade path if a measured limit is hit (F-01).

**Embeddings: none in the first release.** Near-duplicate detection uses shingling and MinHash
(datasketch) and search uses Postgres full text; both run on one core. If semantic search is
wanted later, embeddings are computed on this PC with a pinned open-weight model (bge-m3 or
Qwen3-Embedding-0.6B, F-04) and stored as plain arrays queried offline, or the hosted option is
used; a vector index on the VPS is a Phase 4 decision, not a default.

**Translation: selective, via Claude Haiku.** Language identification with Lingua in its
low-memory mode (Apache 2.0). Titles, extracted claims and quoted spans are translated to
English for display by Haiku 5.5 in the same batch as extraction; full articles are not
translated. No translation model runs on the VPS or on this PC. Original text is always kept and
shown (F-04). The local MADLAD-400 route is the fallback if API translation cost ever matters;
at the volumes in section 12 it does not.

**LLM: the Anthropic API** (user decision, 2026-10-20). Claude Haiku 5.5 for bulk claim
extraction and support checks, Claude Sonnet 5.5 for the harder tier and for assessment drafts,
Opus 5.5 for adversarial review drafts if the operator wants them; the Batch API for anything
that can wait an hour. Model identifier, prompt version and schema version are stored on every
run (section 11). Pricing used in section 12 is the Anthropic first-party table cached
2026-10-06 in the `claude-api` reference.

**Frontend: server-rendered Jinja2 templates from FastAPI with HTMX 2 for partial updates**,
a static SVG world map built from Natural Earth TopoJSON with D3 7, Observable Plot for
sparklines and small multiples, ECharts 6 loaded only on the Trends pages, plain CSS with a
small design-token file for the dark and light themes. No Node process on the server and no
client build step beyond copying pinned, vendored scripts (all MIT, BSD or ISC; versions as of
2026-10-20, F-03). This is the lighter-stack decision of 2026-10-20: one language, one process,
one deployable. The alternative kept as the upgrade path is SvelteKit 3 with MapLibre 6, which
the research priced out (F-03) and which becomes worth its Node runtime only if the map and
charts need interactions HTMX cannot express.

**Reverse proxy and edge: Caddy behind Cloudflare** (the lucascosolo.com zone the user already
runs), Cloudflare caching for public JSON and pages, Cloudflare Access for the operator paths,
and, if the user wants a beta gate, for everything.

## 3. Components and data flow

```
 sources ──> adapters ──> raw store (documents, dataset releases, API responses; immutable)
                              │
                              ▼
                    normalisation (language id, text extraction, dedup digest, geocoding of
                    dataset rows, vintage stamping of observations)
                              │
              ┌───────────────┼──────────────────┐
              ▼               ▼                  ▼
      lineage clustering   observations       claim extraction (quarantined LLM) ──> support check
              │               │                  │
              └──────> events ◄──────────────────┘
                              │
                              ▼
               indicators ──> baselines ──> change detection ──> signals ──> watch rules ──> flags
                              │                                                      │
                              ▼                                                      ▼
                      coverage index                                  operator review ──> assessments
                              │                                                      │
                              └──────────────────────► public API / SSR ◄────────────┘
                                                             │
                                                     calibration & corrections logs
```

Adapters are small modules with one interface: `discover()` (what is new since the cursor),
`fetch(item)` (retrieve and store raw bytes with headers and timestamp), `parse(raw)` (to the
normalised shape), plus a `health()` probe and a declared schedule. Each adapter is registered
with its source record. Dataset adapters (V-Dem, UCDP, World Bank) store each release as a
whole and stamp every observation with the release version and retrieval time (vintage).
Feed adapters (RSS, ReliefWeb, GDELT DOC) store each item and, where allowed, the fetched page.

Normalisation is deterministic code: trafilatura for article text, Lingua for language, courlan
for URL cleaning, dateparser for dates with the source's timezone, a canonical digest of the
cleaned text, GeoNames and Natural Earth joins for places, Wikidata identifiers for actors
resolved from a curated alias table first and from Wikidata search second.

Claim extraction (section 4) produces claims with quoted spans; the support check verifies
each span exists verbatim in the document and asks a second, cheaper pass whether the span
entails the claim; claims failing either check are kept with a `rejected` status for the
extraction gold set, never shown.

Lineage clustering runs over the day's documents and over the trailing window; events are
assembled by rules (same claim type, actor, place and date window across lineages) and by the
operator. Indicators are computed by versioned SQL or Python from observations and events;
baselines and change detection run on schedule; watch rules evaluate on each new signal.

## 4. Where the LLM adds value, and the boundary around it

Deterministic code does everything it can: fetching, parsing, language identification,
deduplication, geocoding of structured data, time-series statistics, rule evaluation, rendering.
The model is used for five things, each with a measurable output:

1. **Claim extraction** from documents into Canary's schema (actor, action type from the
   vocabulary, target, place, time, quoted span, polarity, the evidence category the document
   itself supports). Validated against a hand-coded gold set per language tier and per model
   version (document 09); the literature says this validation is not optional (F-05).
2. **Support check**: does this quoted span entail this claim? A cheap second pass that
   catches the half of unsupported assertions the grounding literature reports (F-05).
3. **Summarisation of long reports** (NGO, UN, observation missions) into claims with page or
   paragraph references, under the same support check.
4. **Translation fallback** for titles, claims and spans where the local model fails.
5. **Drafting** assessments and adversarial reviews for the operator, with every sentence tied
   to a claim identifier; unsupported sentences cannot be saved (document 06, section 5).

The boundary is the CaMeL and dual-LLM rule (F-05): the model that reads untrusted documents has
no tools, no network, no memory of other documents, and returns only structured output that
deterministic code validates; untrusted text never reaches a model that has tools or that
decides anything. Concretely: document text is passed inside a single user message as JSON-encoded
content labelled as untrusted, with a system prompt stating that instructions inside it are data;
output is parsed with a strict schema (structured outputs, `strict: true`); any claim whose
quoted span is not found verbatim in the source is rejected; the operator-facing drafting model
sees only Canary's own claim records, never raw document text; prompt-injection test documents
are part of the test suite and of the extraction gold set (document 09, section 8).

## 5. Storage layout

Four stores in one database, with different write rules (document 08 has the schema):

- **raw** (append-only): for datasets and open-licensed documents, bytes or text with headers,
  URL, retrieval time and adapter version, as files under `~/.cache/canary/raw/` in development
  and on the server's data volume in production, referenced by content digest; for news
  articles, metadata and digests only: the body is processed in memory and not retained
  (document 03, section 8);
- **normalised** (append-only per version): extracted text, language, digests, geocodes, with a
  pointer to the raw record and the normaliser version;
- **derived** (versioned, never updated in place): claims, lineages, events, observations
  (with vintage), indicators, signals, flags, comparisons, each with its run identifier;
- **editorial** (versioned with history): assessments, episodes, source registry overrides,
  corrections; every edit creates a new version row and the previous stays readable.

Article text older than the retention window (default 30 days) is reduced to metadata and
spans by a nightly job; the database stays in the low single-digit gigabytes at the planned
volumes.

Backups: nightly `pg_dump` plus WAL archiving to the storage VPS through the suite's
`storage-backup` protocol with a manifest entry; raw files synced the same way; a restore drill
every quarter is a roadmap acceptance item.

## 6. Scheduling and update cadences

Each source has its own cadence (document 03) and the scheduler respects it: annual datasets are
polled weekly for a new version and ingested once; monthly datasets daily; APIs at their
documented limits (UCDP 5,000 requests a day, ReliefWeb 1,000, HAPI one a second, Cloudflare
Radar per its token); RSS feeds every 30 to 120 minutes depending on their observed update
rate; GDELT DOC queries hourly per watch country and daily for the rest. Change detection runs
after each ingestion of an indicator's source; watch rules run on each new signal; the coverage
index recomputes nightly; the Today payload is regenerated on any assessment publish and at
least hourly. Every job records start, end, items in, items out, errors; a job that produces
zero items when the baseline expects more raises a health alert and marks the source stale.

## 7. Public API

The same JSON the pages render is public, read-only, versioned (`/api/v1/`), rate-limited at the
edge, and documented from the FastAPI schema. Resources: countries, situations, assessments (with
versions), events, claims (with spans and document links), observations (with vintage), indicators,
signals, flags, episodes, comparisons, sources (with health), calibration entries, corrections.
Every response carries the licence and attribution of the sources it includes, so a downstream
user inherits the obligations. Bulk export of Canary's own records under CC BY-SA 4.0 (the most
restrictive share-alike among its open inputs, V-Dem's) is a Phase 4 item.

## 8. Hosting and deployment

Development and all compute (builds, tests, embeddings, translation, backtests) run on this PC,
per the machine context. For serving, three options were weighed:

- **Utility VPS (1 core, 3 GB)**: too small for Postgres with pgvector plus workers plus the
  embedding and translation models; it could host only a static export of the public pages.
- **Production VPS (4 cores, 15 GB)**: has the capacity but is designated for the Hytale servers
  and "nothing heavy"; co-locating Canary's database and workers there breaks that rule and
  couples two unrelated services' uptime.
- **A dedicated small VPS (about 4 vCPU, 8 GB, 80 GB disk)**: the fallback if the utility VPS
  strains; it would cost money and is not planned.

Revised 2026-10-20 (afternoon, then 13:11 CDT): the audience is the user and friends behind
Cloudflare Access, so the load is tiny and the **utility VPS** is the recommendation at no new
cost, with the stack lightened so that everything on the critical path runs there. It already
runs Postgres 17 and the `cloudflared` tunnel that serves the user's other subdomains; it gains
a database, one uvicorn process serving pages and the operator workspace, one Procrastinate
worker process doing fetching, parsing, MinHash, API calls to Anthropic, rules and rendering
jobs, and a tunnel route. Resource budget: Postgres shared buffers raised modestly (256 MB), the
web process about 150 MB, the worker about 250 MB without spaCy or any local model (language
identification with Lingua's low-memory mode; actor and place strings come from the extraction
output and resolve against a small alias table and a GeoNames admin-1 subset held in Postgres);
about 1 GB in total, leaving the other services their share of the 3 GB. Concurrency: two
outbound fetches and two Anthropic calls at a time; feeds polled hourly; extraction volume
capped at about 800 documents a day. This PC is optional: backtests, gold-set evaluation and any
bulk reprocessing run here in a detached session against a database copy, never on the critical
path. Phases 0 and 1 run entirely on this PC; Phase 2 deploys to the VPS. Deployment follows the suite's `deploy`
skill and guard: build here, ship an artifact (a container image or a wheel plus a static
frontend bundle), migrate with Alembic, restart a systemd unit; never build on the server.
Secrets (API keys, tokens) live in mode-600 env files outside the repository, as the suite
requires.

## 9. Security

Untrusted input is every document, every feed and every dataset row. Controls: the LLM boundary
in section 4; strict schema validation of every adapter output; no execution of fetched content;
image and PDF parsing in a sandboxed subprocess with resource limits; URL fetching through an
allow-listed egress with robots.txt and reuse-reservation checks, size limits and timeouts;
dependency pinning with lockfiles and a monthly audit; the operator workspace only behind
Cloudflare Access; the public site read-only with edge rate limits and caching so a traffic
spike is absorbed at the edge; database roles split (ingest-write, derive-write, editorial-write,
public-read); secrets never in the repository; audit log of every editorial action; the harness's
`/security-review` on each completed module (suite rule). Poisoned feeds are handled by the
lineage and independence rules (a single source cannot corroborate itself) and by the health
alerts (a feed whose volume or content distribution shifts abruptly is flagged for the operator).

## 10. Observability

Structured logs (JSON lines) per job and request; metrics for ingestion volume per source,
extraction acceptance rate, support-check rejection rate, lineage cluster sizes, signal counts
per rule, review-queue depth, page latency; a health board in the operator workspace that is the
same data as the public Sources page plus internals; alerts to the operator by the suite's
notification path (Telegram or email) when a source is stale beyond its lag, when extraction
rejection rate jumps, when the queue stalls, or when disk is above a threshold. The public site
never shows a timestamp newer than the last successful run of the thing it displays.

## 11. Reproducibility and versioning of analysis

Every derived record carries a `run_id`; a run records the git commit of the code, the
configuration hash, the model identifier and prompt version (for LLM steps), the embedding
model hash, the indicator catalog version, the watch-rule file version, and the input record
identifiers. Re-running a step with the same versions on the same inputs must reproduce the
outputs; a test asserts this on a fixture. When a method changes, the old outputs are kept with
their run and the new ones are added; the interface shows the current version and links the
history. Observations keep every vintage so backtests can ask "what was known on date D".
Corrections (document 08) are records, not edits.

## 12. Cost model

Assumptions for the lightened stack (revised 2026-10-20, 13:11 CDT), to be replaced by
measurements in Phase 1: 8,000 documents a day discovered; 1,200 fetched; 800 sent to claim
extraction at about 1,500 input and 350 output tokens each; about three claims per document,
each support-checked at 600 input and 100 output tokens; 10 assessment drafts a day at 8,000
input and 1,500 output tokens; translation of titles and spans for 800 documents a day at 300
input and 150 output tokens. Prices are the Anthropic first-party table cached 2026-10-06 (Haiku
5.5 $0.10 input and $0.50 output per million tokens; Sonnet 5.5 $2 and $10; Batch API at half
price). Prompt caching of the instruction block would lower input cost further and is not
counted. The table was produced by the script whose expressions it shows.

| Item | Expression (USD/day) | USD/day | USD/month (30 d) |
|---|---|---|---|
| Claim extraction, 800 docs/day, Haiku 5.5 | `800*1500/1e6*0.10 + 800*350/1e6*0.50` | 0.26 | 7.80 |
| Support checks, 2,400/day, Haiku 5.5 | `2400*600/1e6*0.10 + 2400*100/1e6*0.50` | 0.26 | 7.92 |
| Assessment drafts, 10/day, Sonnet 5.5 | `10*8000/1e6*2 + 10*1500/1e6*10` | 0.31 | 9.30 |
| Translation of titles and spans, 800/day, Haiku 5.5 | `800*300/1e6*0.10 + 800*150/1e6*0.50` | 0.08 | 2.52 |
| **Base case total** | sum of the four rows | **0.92** | **27.54** |
| Base case with the Batch API on extraction and checks | `0.26/2 + 0.26/2 + 0.31 + 0.08` | 0.66 | 19.68 |
| Upper bound (extraction on Sonnet 5.5, no batch) | `5.20 + 0.26 + 0.31 + 0.08` | 5.86 | 175.74 |

Storage at these volumes: text retained for 30 days at `1200*10 KB*30` = 352 MB
rolling; permanent metadata and spans at `1200*2 KB` = 2.3 MB/day, about
0.84 GB/year; no embeddings. Hosting: $0 (the existing utility VPS). The
domain and Cloudflare are already paid. The LLM line is the whole external cost and is well under
$50 a month at these volumes; volume is the lever if the user sets a lower cap.

## 13. What is deliberately not built

A repo-map, context-packing or retrieval layer for the development sessions (suite rule); a
custom forecasting model (document 04, section 11); a graph database; a search cluster; a vector
index; PostGIS; local embedding or translation models; a Node process on the server; a message
broker; user accounts beyond the Access allow-list; a mobile app; real-time websockets (hourly
regeneration is enough for the stated cadences); a scraping fleet (feeds, APIs and bulk files
only, with per-publisher page fetches under their terms).
