# 10. Development roadmap

Phases are ordered so that provenance and analytical correctness come before the dashboard, as
START.md section 15J requires. Each phase names the maturity level it reaches (document 01,
section 6) and the evidence that proves it. Durations are not promised; each phase ends when
its acceptance criteria are met and its evidence is in the repository. Work within a phase is
cut into chunks of one to three tasks for fresh implementer sessions, with contracts and tests
first (suite build loop). All compute runs on this PC; nothing runs on a server before Phase 2.

## Phase 0: Foundations and the first datasets (reaches L2 for datasets)

Objective: a reproducible ingestion spine with provenance and vintages, proven on the open,
negotiation-free datasets, and the state files that let later sessions continue.

Delivers: the Python project (3.13, FastAPI, SQLAlchemy 2.1, Alembic, Procrastinate), Postgres
18 with pgvector and PostGIS in Docker on this PC, the schema for the provenance spine, sources,
documents, dataset releases, observations with vintages, baselines (document 08 sections 1, 2,
4); the source registry YAML with every catalog entry and its `canary_use`; adapters for V-Dem
Country-Year and ERT, UCDP Candidate and GED/ACD (bulk; the API adapter waits for the token),
World Bank Indicators, Our World in Data, EWP SRA, Cline Center coups, and the reference loads
(GeoNames, Natural Earth, ISO, a seed Wikidata alias table); a `canary` CLI (`status`, `ingest
<source>`, `health`); the reproducibility test; JUnit reporting; `.agent/state.json` conventions.

Prerequisites: the user's answers in document 11 to the questions marked "affects Phase 0"
(none block it except the choice to request a UCDP token).

Major decisions already taken: stack (document 07); vintage-mandatory observations; registry as
YAML in the repository.

Difficulties: V-Dem's size (hundreds of columns; load only the catalogued indicators plus the
confidence intervals); UCDP version naming; World Bank per-dataset licences.

Acceptance: every adapter ingests its current release and a re-run produces no new observation
rows (vintage dedup); `canary health` reports each source's freshness; the reproducibility test
passes; `canary status` prints counts per table; every observation traces to a release and a run;
unit tests pass with a JUnit report read by `output-triage`.

Evidence of completion: the test report, the CLI output committed as a fixture, a `DECISIONS.md`
entry per decision taken during the phase.

## Phase 1: Documents, lineages and claims (reaches L3 for the document layer)

Objective: the text pipeline from feeds to validated claims, measured against a gold set, within
a measured cost.

Delivers: the curated feed list (about 200 outlets and NGO feeds, at least twelve languages, each
entry with a reason) as a versioned file; feed, ReliefWeb, GDELT DOC (volume and URL discovery)
and Cloudflare Radar adapters; the fetcher with robots.txt, reuse-reservation and `licence_mode`
handling and Internet Archive save-on-cite; normalisation (trafilatura, Lingua, courlan,
dateparser, geocoding via mordecai3 and GeoNames); lineage clustering (MinHash plus attribution
parsing plus quote matching) with the 500-pair labelled set; the claim vocabulary file; the
extraction gold set for English (300 documents) coded by the operator; Haiku 5.5 extraction with
structured outputs and the support check; the evaluation report per document 09, section 3; the
prompt-injection corpus and tests; translation of titles and spans with MADLAD-400 and Lingua;
local embeddings with bge-m3 pinned by digest; cost measurement against document 07, section 12.

Prerequisites: Phase 0; the Anthropic API key in a mode-600 env file (user decision of
2026-10-20 covers use; the key is the user's to place); ReliefWeb app-name approval requested
(user go-ahead for external requests, document 11).

Major decisions in-phase: extraction model tier per claim type from the measurements; which
languages make tier two; the lineage threshold.

Difficulties: feed churn and paywalls; non-English gold sets (operator time); keeping extraction
spend inside the cap while the feed list is tuned; GDELT duplication.

Acceptance: English extraction meets the targets in document 09 (F1 at or above 0.75 on
institutional and conflict types, span fidelity at or above 0.95); lineage precision at or
above 0.9; injection tests pass; measured daily cost within the user's cap; every claim has a
verbatim span; every fetched page has an archive capture or a recorded reason why not.

Evidence: the evaluation report committed under `docs/evaluations/` with model, prompt and gold
set versions; the cost measurement; the test report.

## Phase 2: Indicators, signals, coverage, and the first interface (reaches L3 overall)

Objective: the three layers visible for every country, honestly labelled, on a private beta at
the public hostname.

Delivers: the indicator catalog v1 (about twenty indicators across the domains, each with
baseline and detection parameters), baselines at three horizons, change detection, the
coverage index with its label rule, the watch-rule file with the first rules written but
disabled; the stable-period false-alarm review (ten country-years) and its calibration-log
entries; the SvelteKit application with Today, Map (tile-free), Country, Situation (read), Trends,
Sources, Methodology and the corrections and calibration pages; the public API v1; the operator
workspace (review queue, assessment editor with the eight fields and the checklist, source
registry editor); deployment to the dedicated VPS behind Cloudflare Access with the heavy steps
scheduled on this PC; backups to the storage VPS with a manifest entry and one restore drill.

Prerequisites: Phase 1; the user's hosting decision and spend approval (document 11); the
Cloudflare DNS and Access setup through the `cloudflare-control` skill; the `deploy` skill's guard.

Major decisions in-phase: which rules are enabled after the review; the exceedance thresholds
chosen by noise-to-signal on the available history; theme defaults.

Difficulties: making the five channels (urgency, severity, confidence, trend, completeness)
legible without a score; the operator's review queue depth; a public hostname before public
launch (the Access gate handles it).

Acceptance: every Today item answers the eight questions and links to evidence in two clicks;
every country page shows the coverage label and freshness per source; no composite number
anywhere (a test greps the rendered pages for the forbidden patterns); performance budgets met
on the target host; rules enabled only with a logged review; restore drill passed; `/security-review`
run on the deployed modules; accessibility keyboard pass.

Evidence: screenshots of the eight-question card and a situation page committed under
`docs/evaluations/`; the false-alarm review entries; the deploy ledger.

## Phase 3: History, comparisons, and public launch (reaches L4 in part)

Objective: the historical layer and the editorial workflow complete enough to publish to the
world, with the legal and reader checks done.

Delivers: twelve or more episodes with cited milestones (at least four reversal or resilience
cases); the comparison editor with the Neustadt-May fields and the required sentence; the
deterministic matcher and its outcome-blind test; the assessment workflow with Claude drafts
tied to claim identifiers and the review checklist enforced; the corrections and calibration
logs populated; attribution rendering audited source by source; the additional sources whose
licences were confirmed in the meantime (Freedom House, CIVICUS, RSF, OpenSanctions, UNHCR, IPU
Parline, ElectionGuide, OONI, #KeepItOn); the media-lawyer consultation and its outcome recorded;
the five-reader test and the copy changes it produced; the accessibility audit in both themes;
the external read (document 09, section 11) invited.

Prerequisites: Phase 2; the user's approval to publish (publishing gate); confirmed licences
for each added source (written permission where the catalog says "permission").

Difficulties: operator time to write episodes well; the temptation to launch before the
reversal cases are written (the acceptance criterion prevents it); legal review cost.

Acceptance: the success criteria of document 01, section 10, all met; the Access gate removed
only after the user's explicit go.

Evidence: the launch checklist with each criterion linked to its evidence; the first calibration
log entries; the reader-test notes.

## Phase 4: Backtesting, calibration and expansion (L4, toward L5)

Objective: know how well the signals and rules would have done, publish it, and widen coverage.

Delivers: the as-of replay harness (vintage queries, GDELT and Media Cloud date-bounded discovery,
Internet Archive captures); backtests on twelve episodes and ten stable years with detection
probability, lead time, false-alarm ratio and precision-recall per rule and method; rule tuning
with every change logged; the symmetry and ablation tests; the external review responses
published; language tiers two and three with their gold sets; national legislative adapters for
the six jurisdictions with APIs and the `legislation` entity; Media Cloud integration; ViEWS and
EWP shown as external models with their precision; JSON-LD export of the episode library; saved
searches and watchlists for the operator; the first yearly re-read of episodes.

Prerequisites: Phase 3; Media Cloud key; any permissions obtained (ACLED aggregates, IOM) if
the user chose to ask.

Acceptance: the calibration log carries the backtest results; no enabled rule lacks a backtest
entry; tier-two extraction meets its targets; symmetry tests pass or their failures are logged
with fixes.

Evidence: the backtest report under `docs/evaluations/`; the review correspondence (with
permission) or its summary.

## Phase 5: Validated early warning, if the evidence allows (L5)

Objective: claim early-warning capability only for what the backtests support, and keep
improving monitoring regardless.

Delivers, conditionally: any learned or statistical model that beat the published models and
the simple rules on precision at a stated lead time in Phase 4, deployed as an external-model
panel with its base rate and precision, never as a score; subnational coverage where sources
allow; a contributor workflow (second editor, review roles) if contributors appear; a yearly
methodology revision with external review.

Acceptance: a model is shown only with a calibration-log entry demonstrating its out-of-sample
performance; the roadmap is revised from the Phase 4 results and the user's priorities.

## Cross-phase rules

- Every phase ends with `DECISIONS.md` entries, a `docs/12-handoff.md` revision, a pruned
  `.agent/state.json`, a pushed `main`, and a session boundary (suite rule on milestones).
- No phase adds a composite score, an autonomous publication path, or a scraping fleet.
- Cost is measured monthly against the cap from Phase 1 onward; a breach stops extraction
  volume growth, not ingestion.
- Any source whose licence changes drops to links-only within one day of the change being
  noticed, with a corrections-log entry.
