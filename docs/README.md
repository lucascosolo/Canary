# Canary: development specification

Canary is a free, public, non-profit command center for early recognition of threats to democracy,
human rights, civil liberties, peace and social cohesion anywhere in the world, built so that every
assessment shows its evidence, its uncertainty and its historical context. This directory is the
specification produced in the initiation session of 2026-10-20 from the brief in `START.md`. It is
written for the next Claude Code sessions, which will implement it, and for the user, who decides.

Status: a design proposal with research behind it, not a validated system. Each document labels
verified findings (with the research note that holds the citation), the author's recommendations,
and open questions. Decisions the user still has to take are collected in `11-risks-and-open-questions.md`
and in `../DECISIONS.md` under "Provisional".

## Reading order

| Document | What it settles |
|---|---|
| `01-vision-and-requirements.md` | What Canary is and is not, who it is for, the eight questions every warning answers, the five maturity levels, success criteria |
| `02-research-landscape.md` | What exists already (indices, event data, monitoring platforms, academic frameworks, early-warning practice in other fields), what is reusable, where the gaps are |
| `03-data-source-catalog.md` | Every source evaluated, with access, licence, cadence, limits and priority; the first-integration set; the source-registry design |
| `04-analytical-framework.md` | The three-layer model (baseline, change, assessment), evidence records, source independence, confidence language, watch rules, worked examples |
| `05-historical-knowledge-strategy.md` | The episode library, the comparison procedure, base rates, validation |
| `06-ui-information-architecture.md` | Views, navigation, progressive disclosure, how urgency, severity, confidence, trend and completeness are shown separately |
| `07-technical-architecture.md` | Stack, components, data flow, LLM boundaries, hosting options, costs, observability, security |
| `08-data-model.md` | Entities, provenance, append-only rules, corrections |
| `09-validation-and-testing.md` | Tests at every level, extraction gold sets, backtesting without look-ahead, bias checks, the public calibration log |
| `10-roadmap.md` | Phases 0 to 5 with objectives, prerequisites, acceptance criteria, evidence of completion |
| `11-risks-and-open-questions.md` | Ranked risks with mitigations; decisions that need the user |
| `12-handoff.md` | What the next session does first |

Evidence: `research/notes/` holds the verbatim researcher returns (36 notes, each with URLs and the
date read). A claim in these documents that cites a note (for example "note B-01") is traceable to
a page read on 2026-10-20; a claim without one is the author's recommendation or a fact the
author considers settled and has marked as such.
