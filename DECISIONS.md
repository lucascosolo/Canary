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
