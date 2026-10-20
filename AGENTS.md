# Canary: agent instructions for this repository

Canary is a global early-warning and historical-pattern-analysis command center. The founding
brief is `START.md`; read it before any substantial work. The development specification lives in
`docs/` and the decision log in `DECISIONS.md`. Until `DECISIONS.md` records that the user has
approved the first implementation phase, this repository is a specification, not an application:
do not start building the system.

## File-safety rules (from START.md, non-negotiable)

- **Never execute `rm` in any form**, and never introduce scripts, Makefile targets, package
  scripts, hooks or cleanup routines that execute `rm`, `rmdir`, `shutil.rmtree`, `os.remove`,
  `fs.rm`, the delete action of `find`, `git clean` or equivalents.
- A file that genuinely needs removing is moved into `quarantine/<YYYY-MM-DD>/` (gitignored)
  with `mv`, and its permanent deletion is left to the user.
- No destructive git: no force-push, no history rewriting, no hard resets on shared branches.
- Do not assume pushing is authorised. The remote, once one exists, is recorded in
  `DECISIONS.md`.

## Documentation layout

| Path | Purpose |
|---|---|
| `START.md` | The founding brief. Never edit; it is the user's statement of intent. |
| `docs/README.md` | Index of the specification and reading order. |
| `docs/01` … `docs/12` | The specification documents (vision, research, sources, analysis, history, UI, architecture, data model, validation, roadmap, risks, handoff). |
| `docs/research/notes/` | Raw research returns from researcher agents, one file per question, dated. Evidence for the claims in `docs/02` and `docs/03`. Never edited after the fact; add a new dated note instead. |
| `DECISIONS.md` | Architecture and product decisions: date, decision, alternatives, reasons, what would reopen it. Append-only; mark superseded entries rather than deleting them. |
| `.agent/` | Working state for agent sessions (`state.json`, `log.jsonl`, `handoff.md`), gitignored. |

## Conventions for the specification

- Every factual claim about an external source (a license, an API, a cadence, a price) cites the
  URL read and the date it was read. A claim without a date is treated as unverified.
- Verified findings, the author's recommendations, and open questions are labelled as such and
  never mixed in one sentence.
- Dates are ISO-8601. Country references use ISO 3166-1 alpha-3 codes alongside names.
- The specification is internally consistent: the data model in `docs/08` is the one the
  architecture in `docs/07` and the roadmap in `docs/10` refer to. A change in one is a change
  in all.

## Working rules

- Small, reviewable commits with descriptive messages; commit at every working checkpoint.
- Research notes and design decisions are version-controlled, not kept in chat.
- When a spec change depends on a decision the user has not made, record the assumption in
  `DECISIONS.md` under "Provisional" and proceed; do not silently decide an irreversible point.
