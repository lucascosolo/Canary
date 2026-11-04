# Phase 0 plan

Acceptance is in `docs/10`, Phase 0. Chunks follow `docs/12`, cut by what can be verified.

| Chunk | Deliverable | Verification | Needs a database | Status |
|---|---|---|---|---|
| scaffold | pyproject, lockfile, licences, Compose, Alembic baseline, CLI entry point, test reporting | `uv run pytest`; `uv run alembic upgrade head --sql` | no | complete |
| registry | Registry YAML format, validating loader, `canary registry validate`, entries for the P0 sources | `uv run pytest`; `uv run canary registry validate` | no | complete |
| spine | `pipeline_run`, `source`, `source_version`, `source_health`, `dataset_release`; `canary health` | `db` tests | yes | complete |
| observations | `indicator`, partitioned `observation`, `baseline`; as-of helper; vintage dedup; reproducibility test | `db` tests | yes | complete |
| adapters | V-Dem Country-Year and ERT; UCDP bulk; World Bank; Our World in Data; EWP SRA and Cline coups; reference loads | each adapter ingests, a re-run adds no rows | yes for acceptance | blocked |
| status | `canary status`; acceptance evidence committed | `docs/10` acceptance list | yes | blocked |

## What the terms re-check changed (notes H-03 and H-04, 2026-11-04)

- **V-Dem ERT is cleared** under its package licence, by note H-05, which supersedes the earlier verdict.
- **#KeepItOn and the Global Legal Monitor stay links-only**, which reaches Phase 1, not Phase 0.
- **ISO 3166 needs no adapter of its own.** The reference load takes alpha-3 codes from Natural Earth,
  which the registry records as open.
- **The other Phase 0 adapters are clear**: V-Dem Country-Year (from GitHub, not the website form), UCDP, World Bank, Our World in Data
  (an allow-list, empty until a series is cleared), the Early Warning Project (shown unchanged) and Cline Center coups.

## The test-database question

Resolved 2026-11-04: the user chose option 1. The rest of this section is kept for the record.

The test database needs a real PostgreSQL that an agent can start inside its sandbox, which means
TCP on loopback and pg_trgm available. Options:

1. **Install PostgreSQL 17 from the PGDG apt repository (recommended).** Same major version as the
   utility VPS, signed packages, and an agent starts its own server from `/usr/lib/postgresql/17`
   with a data directory under `~/.cache/canary/`. The user runs the install because it needs sudo.
2. **Install Ubuntu's PostgreSQL 18.** One command with no new repository, but one major version
   ahead of the VPS, so a migration could pass here and fail there.
3. **Allow the theseus-rs PostgreSQL 17 tarball.** No sudo and the right version, but it runs a
   third-party build, and it needs a permission rule the user adds.

Docker is not an option for agent sessions: the sandbox refuses its socket. `compose.yaml` remains
for the user's own runs outside the sandbox.
