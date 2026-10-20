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

## 2026-10-20 — Specification delivered; provisional assumptions it proceeds on

The twelve documents under `docs/` are complete as a proposal. They proceed on these
assumptions, each put to the user in `docs/11-risks-and-open-questions.md` section 2:

- Hosting on a dedicated small VPS from Phase 2 (spend decision pending); Phases 0-1 on this PC.
- An external spend cap of about $100 a month, with the base case computed at about $59.
- A Cloudflare Access beta gate during Phase 2.
- Credentials and permissions (UCDP token, ReliefWeb app name, Media Cloud key, ElectionGuide,
  ACLED and HDX written questions) requested only after the user's yes.
- Global scope with about twelve languages in the first feed list.
- Symmetric editorial rules for every country, including the United States.
- Code under Apache 2.0, Canary's own data and text under CC BY-SA 4.0.
- The name "Canary".

Superseded entries: "Repository initialised locally; remote deferred" is superseded by the
remote entry above.

## 2026-10-20 — Audience, access and legal posture revised (user input, afternoon)

Recorded from the user on 2026-10-20 (13:07 CDT): "I'd rather just publish it under my name as a
little web tool to share with friends. I'm not requesting official permission, access or tokens
from any entities, and I don't want this to do anything that might get me in legal trouble."

This supersedes the morning entry "free, public, non-commercial, non-profit" on three points and
keeps the rest:

- Audience: the user and a small circle of friends, behind Cloudflare Access with an allow-list.
  Not open to the public. No legal entity, no external reviewers, no launch gate; "launch" means
  sharing the link.
- Sources: only those usable without registration, credentials, tokens or permission, and only
  those whose licence is explicit and permits storage and display for personal non-commercial
  use. Everything else is a link. No emails or forms to any organisation. A token from the
  user's own existing account (Cloudflare) is the one exception, and the user may strike it.
- Legal posture: minimise exposure rather than consult a lawyer. Concretely: no article full text
  retained after processing (metadata, a short quoted span and the extracted claim only);
  robots.txt and machine-readable reuse reservations honoured; no paywall or login circumvention;
  licensed-open datasets only; assessments name institutions and offices, and individuals only
  in official capacity for documented official acts; no allegations about individuals beyond
  what a legal finding or official document states; a visible disclaimer and a contact for
  corrections.

Consequences applied in `docs/01`, `03`, `04`, `07`, `09`, `10`, `11`, `12` as a dated revision.
Hosting moves to the existing utility VPS (no new spend) with heavy steps on this PC.

## 2026-10-20 — Lighter stack for the utility VPS; evidence-standard content rules (user input, 13:11 CDT)

Recorded from the user: "make it a lighter process so it can run on the utility VPS comfortably
if possible" and "since it's a private tool where I can control access, surely it doesn't need
to be super conservative in the content".

Decisions applied:

- Stack lightened (docs/07): no pgvector, no PostGIS, no local embedding or translation models,
  no Node process on the server. One Python service (FastAPI with Jinja2 templates and HTMX) and
  one worker process on PostgreSQL 17 with pg_trgm and built-in text search. Duplicates by MinHash;
  search by Postgres full text; translation of titles and spans by Claude Haiku; the world map a
  static SVG from Natural Earth TopoJSON. Target footprint on the VPS: about 1 GB of RAM for
  Canary's three processes combined, extraction volume about 800 documents a day. This PC is
  optional (backtests, gold-set evaluation, bulk reprocessing), never on the critical path.
- Content rules are evidence standards, not legal minimisation (docs/04 section 9): individuals
  may be named where the cited evidence supports it, with the evidence category shown; claims
  keep a quoted passage; opinions stay tied to cited facts; no speculation about motives. Article
  text is retained for a configurable window (default 30 days) for re-processing and operator
  reading, then reduced to metadata and spans, for size rather than legal reasons. The
  disclaimer and corrections contact stay because they cost nothing.
- Unchanged: no credentials or requests to any organisation; friends-only access; no public launch.
