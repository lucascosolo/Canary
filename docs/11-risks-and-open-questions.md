# 11. Risks and open questions

## 1. Risks, ranked by consequence

1. **A published assessment is wrong and harms someone or something: a person's reputation, a
   country's standing, Canary's credibility.** Technical: human review before publication, the
   checklist for strong statements, confidence inputs shown, corrections traceable, no scores,
   opinion-on-disclosed-facts structure (G-02). Tested by: the review checklist, the symmetry
   test, the reader test. Residual: real; a media-lawyer consultation is a Phase 3 item and the
   user should decide whether Canary operates under a formal non-profit entity (question 8).
2. **Coverage bias makes Canary a Western-media monitor with a world map.** Mitigation: the
   curated multilingual feed list as a first-class artifact, the coverage index on every country,
   the "no data is not no event" rule, local and regional sources prioritised where
   international coverage is thin (START.md section 8). Tested by: ablation and geographic
   consistency tests. Residual: gold sets for many languages need operator time.
3. **Licence breach.** A third of the catalog has unverified or restrictive terms; ACLED's EULA
   and the UN's terms are stricter than commonly assumed. Mitigation: `canary_use` enforced at
   render, written permissions before storing restricted data, the excluded list, attribution
   text per source, a links-only fallback within a day. Tested by: the render-time licence check.
4. **Extraction error and model drift.** Mitigation: gold sets per tier and model version, the
   support check, held claim types, quarterly re-validation, run versioning. Tested by: document
   09, section 3. Residual: the codebook-following problem (F-05) means headline F1 can mislead;
   the remapped agreement check is mandatory.
5. **False alarms and alert fatigue, or the opposite, a silence read as calm.** Mitigation: rules
   disabled until the stable-period review; the calibration log; the suppression flag; vintage
   backtests. Residual: rare events mean few test cases; honesty about that in the log.
6. **Prompt injection and poisoned feeds.** Mitigation: the quarantined extractor with no tools,
   strict schemas, verbatim-span requirement, injection corpus in the tests, lineage rules that
   stop a source corroborating itself, health alerts on distribution shifts (F-05, document 07
   section 9).
7. **One operator.** Everything editorial depends on the user's time. Mitigation: automation
   proposes and never publishes, so an absent operator produces a stale-but-honest site rather
   than a wrong one; freshness stamps; queue caps; the roadmap sized to one person; a contributor
   workflow deferred to Phase 5. Residual: the historical library's pace.
8. **Sources disappear or change.** Already observed during this research (IMF portal retired,
   ReliefWeb app names, CPJ API offline, POLECAT stale, ACLED's access model). Mitigation: health
   checks with schema digests, the registry lifecycle, vintages so history survives, adapters as
   small isolated modules.
9. **Political pressure and accusations of bias, including over coverage of the United States.**
   Mitigation: identical rules for every country, published methodology and rule file, the
   symmetry test, evidence on the same screen as every conclusion, corrections in public. This is
   the project's premise (START.md section 6) and the strongest defence is the visible evidence.
10. **Misleading historical analogies.** Mitigation: the comparison procedure, the required
    sentence, the outcome-blind matcher test, a third of the library as reversal or resilience.
11. **Cost creep.** Mitigation: the measured cost model (document 07, section 12: about $59 a
    month at the base assumptions, about $39 with the Batch API, an upper bound near $430 if
    everything ran on Sonnet), a hard cap, volume as the lever.
12. **Public-site abuse and outages.** Mitigation: read-only public surface, edge caching and rate
    limits, no reader accounts, backups with a quarterly restore drill.
13. **Data loss on this PC.** Mitigation: pushed `main` after every commit, the suite's hourly
    home snapshots, the storage-VPS backup protocol from Phase 2.
14. **Over-building.** Mitigation: the monolith rule, the list of things not built (document 07,
    section 13), phases that end at acceptance criteria rather than feature lists.

## 2. Decisions that need the user

Each is stated with the recommendation and what it affects. Answers go into `DECISIONS.md`.

1. **Hosting and spend (affects Phase 2).** Approve a dedicated small VPS (about 4 vCPU, 8 GB)
   from the existing provider for Canary from Phase 2, with heavy steps on this PC. Alternatives:
   co-locate on the production VPS against the machine rules; or static-only on the utility VPS
   with no live pipeline. Recommendation: the dedicated VPS. This is a spending decision and is
   gated on an explicit yes.
2. **Monthly external-spend cap (affects Phase 1).** Recommendation: a cap of $100 a month for
   the Anthropic API plus any hosted service, with the base case at about $59 and the Batch API
   bringing it to about $39 (document 07, section 12); extraction volume is throttled to stay
   under it.
3. **Beta gate (affects Phase 2).** Recommendation: Cloudflare Access on the whole site during
   Phase 2, removed at the Phase 3 launch gate.
4. **Requests made in the user's name (affects Phases 0 to 3; external communications gate).**
   The UCDP API token (email to the maintainer); ReliefWeb app-name approval; a Media Cloud key;
   ElectionGuide credentials; a written question to ACLED's Access team about what a public
   non-profit site may display; a written question to HDX about ACLED-derived fields in HAPI;
   the Cloudflare Radar token from the user's existing account; later, Freedom House's data
   request and IOM's permission if wanted. Recommendation: send the UCDP, ReliefWeb and
   Cloudflare ones now, the rest when their phase starts. None is sent without the user's yes.
5. **Scope emphasis (affects Phase 1).** Global with twelve languages is the recommendation; the
   user may name regions or countries that should have denser feeds from the start.
6. **Editorial policy (affects Phase 2).** Confirm: symmetric rules for every country including
   the United States; actors named only in public roles; no probabilities of Canary's own; the
   prohibited-phrase list. Recommendation: confirm as written in document 04.
7. **Licences for Canary's own outputs (affects Phase 2).** Recommendation: code under Apache
   2.0 (so that reuse is easy and pg_search's AGPL, if ever adopted, is a separate decision);
   Canary's own data and text under CC BY-SA 4.0, matching V-Dem's share-alike which Canary's
   episode library inherits.
8. **Legal entity (affects Phase 3).** Whether Canary publishes under an incorporated non-profit
   or under the user personally; this changes liability and some licence eligibility (research
   organisation status under EU TDM rules, G-02). Recommendation: take the media-lawyer
   consultation in Phase 3 with this question on the agenda.
9. **Name.** "Canary" is used throughout; confirm or rename before Phase 2's public hostname.
10. **Git remote.** The sandbox cannot write `.git/config`; run
    `git remote add origin git@github.com:lucascosolo/Canary.git` outside it (`!` prefix) so
    future sessions can push with the bare `git push origin main`.
11. **External reviewers (affects Phase 3).** Whether the user is willing to invite two or
    three domain readers before launch, and whether their comments may be published.
12. **Session model.** The user has said the implementation will be orchestrated on Opus 5.5;
    the handoff (document 12) is written for that.

## 3. Questions the research left open (no user decision needed; next session with a browser)

Listed in document 02, section 4: terms and access details for EIU, IPC manual 3.1, CrisisWatch,
UN Digital Library OAI-PMH, ACAPS, INFORM, IDMC, WFP, FEWS NET, ACLED tier limits, HDX on ACLED
fields, IPU Parline licence, Constitute, Freedom House request flow, RSF licence, CIVICUS data
licence, OONI endpoints, IODA, Metaculus terms, V-Dem U-turn figures, the Admiralty doctrine
text, ERT codebook variables, GTD's current regime, WJP licence, psdata.un.org contents,
UNHCR terms.
