# 12. Implementation handoff

For the next Claude Code session (the user intends to orchestrate implementation on Opus 5.5).
Read this, then `AGENTS.md`, then `DECISIONS.md`, then the documents this file points to. Do not
re-run the discovery: the research notes and the specification are the record.

## What has been decided

- Product: a free, public, non-profit, evidence-first monitor; no composite scores; no
  autonomous publication; three layers shown side by side (documents 01 and 04).
- Audience: the user and friends, behind Cloudflare Access at `canary.lucascosolo.com`, hosted
  on the existing utility VPS from Phase 2 with heavy steps on this PC; no new spend; no legal
  entity; no external requests of any kind (DECISIONS.md, afternoon entry of 2026-10-20).
  Phases 0 and 1 run on this PC only.
- LLM provider: the Anthropic API (user, 2026-10-20). Default tiers: Haiku 5.5 for extraction
  and support checks, Sonnet 5.5 for drafts; model and prompt versions recorded on every run.
- Stack (lightened 2026-10-20, 13:11 CDT, to run on the 1-core, 3 GB utility VPS): Python
  3.13, FastAPI with Jinja2 and HTMX, SQLAlchemy 2.1, Alembic, Procrastinate, PostgreSQL 17 with
  pg_trgm and built-in full text; MinHash for duplicates; static SVG map from Natural Earth; Haiku
  for extraction, support checks and translation; no vector index, no PostGIS, no local models,
  no Node on the server (document 07). Budget about 1 GB of RAM for Canary's processes.
- Data model and append-only rules in document 08; validation targets in document 09.
- Source policy: the catalog in document 03 with `canary_use` per source and the
  no-credentials, minimal-legal-risk rules of its section 8; only keyless, explicitly licensed
  sources are stored; news bodies are processed in memory and not retained; ACLED, GTD, COW,
  Manifesto, ReliefWeb, commercial news APIs and bulk UN documents are out or links-only.
- Repository: `main` on `github.com/lucascosolo/Canary`, pushed by URL because the sandbox
  cannot write `.git/config` (document 11, question 10).

## First implementation objective: Phase 0

Deliver the ingestion spine on this PC (document 10, Phase 0). Suggested chunking for fresh
implementer sessions, each with a contract and tests written first by `test-author`:

1. Project scaffold: `pyproject.toml` (Python 3.13 pinned), `uv` lockfile, Docker Compose for
   Postgres 17 (plain; matching the VPS), Alembic baseline, the `canary` CLI skeleton, JUnit
   test reporting, `.agent/` conventions. No application logic.
2. Provenance spine and registry: `pipeline_run`, `source`, `source_version`, `source_health`,
   `dataset_release`, the registry YAML loader with validation of `canary_use` and
   `terms_verified_on`, the `canary health` command.
3. Observations with vintages: `indicator`, `observation` (partitioned), `baseline` tables, the
   as-of query helper, the vintage dedup rule, the reproducibility test harness.
4. Dataset adapters, one chunk each: V-Dem Country-Year plus ERT (selected columns and
   intervals); UCDP Candidate and GED/ACD bulk (no API); World Bank Indicators API (keyless);
   Our World in Data; EWP SRA CSV plus Cline coups; reference loads (GeoNames, Natural Earth,
   ISO, Wikidata alias seed).
5. `canary status` and the first `DECISIONS.md` entries from the phase.

Acceptance for the phase is in document 10. Do not start Phase 1's feed list or extraction
until Phase 0's acceptance evidence is committed.

## Before the first chunk

- Ask the user the remaining questions from document 11 (spend cap, scope emphasis, editorial
  policy confirmation, output licences, name). Nothing is requested from any organisation, ever.
- Confirm the Anthropic API key location (a mode-600 env file outside the repository) when
  Phase 1 begins, not before.
- Read `~/.agents/context/machine.md` and `engineering.md` before writing any install or build
  command (suite rule); builds, Docker and tests run on this PC only.
- Keep research notes untouched; add new dated notes for anything re-verified in a browser
  (document 02, section 4 lists what needs it).

## Constraints that do not change

No `rm` in any form (quarantine instead); no force-push; no composite score; no model
publishing anything; licence mode enforced at render; article text reduced to spans after the
30-day window; no credentials or requests to any organisation; evidence-standard naming with
the evidence category shown (document 04, section 9); the VPS resource budget; vintages on every
observation; every derived row carries a run id; small commits pushed after each; `DECISIONS.md`
for every choice; the three gates (spend, production deploy, external communication) need an
explicit yes each time.

## Where things are

- `START.md`: the brief. `AGENTS.md`: repository rules. `DECISIONS.md`: decisions and
  provisional assumptions.
- `docs/01` to `docs/11`: the specification. `docs/research/notes/`: 38 dated research notes.
  `docs/design_mockups/`: the user's two reference mockups.
- `.agent/state.json` and `.agent/log.jsonl`: session state (gitignored); `.agent/handoff.md`
  mirrors this document for the harness.
