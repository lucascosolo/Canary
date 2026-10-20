# Decisions

Append-only. Each entry records the date, the decision, the alternatives considered, the reasons,
and what would reopen it. Superseded entries are marked, never removed. Entries under
"Provisional" are assumptions the specification proceeds on until the user confirms or changes
them.

## 2026-10-20 — Repository initialised locally; remote deferred

Decision: `git init` on `main`, with small commits at each checkpoint. No remote has been
created. Alternatives: create a private GitHub repository immediately (the suite's standing rule
for repositories without a remote) or wait. Reason: START.md says not to assume pushing is
authorised when the state is unclear, and the repository did not exist before this session; the
user's hourly home-directory snapshots cover the interim. Reopened by: the user naming a remote,
or approving the creation of a private `lucascosolo/canary` repository.

## 2026-10-20 — Hosting target: canary.lucascosolo.com (user input)

Recorded from the user on 2026-10-20: the project will be hosted at `canary.lucascosolo.com`.
Consequences the specification takes from this: the application is publicly reachable on the
user's existing Cloudflare-fronted infrastructure (the lucascosolo.com zone), so the design must
assume a public hostname from the first deployed phase, and the deployment and access-control
sections treat "behind Cloudflare Access with a login" versus "open to the public" as the
remaining decision. Not decided by this input: which host runs it, whether it is open to the
public, and whether it is a commercial product.

## 2026-10-20 — Research method for this specification

Decision: research is done by `researcher`-tier agents answering one narrow, source-specific
question each, returning a cited answer; the orchestrating session records each answer verbatim
under `docs/research/notes/` and does the synthesis itself. Alternatives: a single long research
agent per theme (loses citations and overflows context), or the harness's deep-research
procedure with general-purpose agents (forbidden by the suite's delegation rules). Reason: the
brief requires that claims be cited and dated and that findings be reconciled rather than
accepted; narrow questions make each answer checkable. Reopened by: nothing; this is a process
note.

## Provisional (awaiting the user)

Entries here are assumptions the specification proceeds on. Each is also listed in
`docs/11-risks-and-open-questions.md` with the question put to the user.

(filled in as the specification is written)

## 2026-10-20 — Audience and licensing posture: free, public, non-commercial, non-profit (user input)

Recorded from the user on 2026-10-20: "this will just be a free to access dashboard for everyone,
no commercial intent. Non profit." Consequences the specification takes from this: sources whose
terms permit non-commercial use with attribution are in scope (Freedom House data, OpenSanctions
under CC BY-NC, CPJ text under CC BY-NC-ND for links and citations); sources that forbid
redistribution regardless of purpose (Polity5, PITF, EIU, ACLED raw events) are used only as
backtesting inputs, as links, or after written permission; there is no login for readers, so the
system must tolerate public load and must treat every published assessment as a public statement
(human review before strong warnings, visible evidence, corrections traceable). Not decided by
this input: whether the user wants a reader-facing "beta" gate (Cloudflare Access) during early
phases, and what monthly budget the non-profit operation can bear.

## 2026-10-20 — Remote: github.com/lucascosolo/canary (user-created)

The user created the repository `lucascosolo/canary` on GitHub and asked for the work to be
pushed there. The remote is added as `origin` over SSH and `main` is pushed. This supersedes the
"remote deferred" entry above. Pushes follow the suite rule: after every commit, as a bare
`git push origin main` from the repository folder.

## 2026-10-20 — LLM provider: the Anthropic API (user input)

Recorded from the user on 2026-10-20: "Canary can use the anthropic API to do LLM calls if
necessary." Consequences: the extraction, support-check, translation-fallback and drafting roles
in `docs/07` are specified against the Anthropic Messages API with model and prompt versions
recorded on every run; a monthly spending cap and the choice of default tier (Haiku 5.5 for bulk
extraction, Sonnet 5.5 or Opus 5.5 for review drafts) remain for the user to confirm in `docs/11`.
