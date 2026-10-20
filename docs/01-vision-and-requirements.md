# 01. Vision and product requirements

## 1. The problem

Dangerous political developments rarely announce themselves. Democratic erosion in the current
wave proceeds through legal, incremental steps taken by elected governments rather than through
coups or election-day fraud (Bermeo 2016; Lührmann and Lindberg 2019; note D-01). Mass-atrocity
risk is dominated by slow structural factors, with onsets so rare (fewer than two state-led
onsets a year worldwide since 1945, note D-02) that any system claiming to predict them will be
wrong almost every time it raises an alarm. Conflict escalation is forecastable where conflict
already exists and nearly unforecastable where it does not (Cederman and Weidmann 2017; Mueller
and Rauh 2022; note D-03). Meanwhile the reporting that would reveal these developments is
uneven: syndicated, concentrated in a few languages, suppressed where it matters most, and
revised after the fact (notes B-03, B-05, G-01, A-04).

The existing landscape has excellent pieces and no whole. Annual indices (V-Dem, Freedom House,
International IDEA, RSF) describe where a country stands but arrive once a year. Event datasets
(UCDP, ACLED, GDELT) count violence or attention but not institutional change. Curated monthly
trackers (International IDEA's Democracy Tracker, Crisis Group's CrisisWatch) are human-written,
not machine-readable, and do not show their evidence. Expert early-warning surveys for democracy
exist only for the United States. Commercial platforms are closed. The research survey found no
open, cross-domain, evidence-showing monitor with a documented methodology (note F-06).

## 2. What Canary is

Canary is a public, free, non-profit situational-awareness system. It monitors indicators of
democratic erosion, repression, conflict escalation, information control, economic stress and,
equally, institutional resilience and de-escalation, across every country; it places each
development in its country's own baseline and in documented historical context; and it shows,
for every assessment it publishes, the evidence, the sources, how independent those sources
are, what is uncertain, what is missing, and what would change the assessment.

Canary is not a prediction engine, a risk index or a news aggregator. It does not publish a
"risk score". It does not forecast coups, wars or breakdowns. Where a published model with
published accuracy exists (the Early Warning Project's statistical risk assessment, ViEWS), Canary
shows that model's output with its base rate and its own stated precision; it does not add a
model of its own until a backtest, run without look-ahead, says one would help (document 09).

The one-line statement for the site: *Canary watches the world for the early signs that
democracies, rights and peace are coming under strain, or recovering, and shows you the evidence.*

## 3. Who it is for

Three audiences, in priority order for the first public release:

1. **The user and a small circle of friends** who want a five-minute daily picture of what
   changed, where, why it matters and how sure anyone can be. Behind a Cloudflare Access login
   with an allow-list; not open to the public (user decision of 2026-10-20, afternoon,
   superseding the morning's "free to access for everyone").
2. **The investigator**: journalists, researchers, civil-society analysts, students, who want to
   go from a headline to a country, a situation, a source, a time series, a historical parallel,
   and leave with citations.
3. **The operator**: the user, who curates sources, reviews automated flags, writes or approves
   assessments, and maintains the historical library. A single-editor workflow at first; the data
   model does not preclude more editors later.

Not an audience: the general public (no public launch is planned), governments or institutions
needing alerts with service guarantees, and anyone wanting country-level probabilities.

## 4. Primary use cases

- **Daily overview.** "What is new, worsening or improving since yesterday, and what deserves
  attention?" Served by the Today view (document 06).
- **Country investigation.** "What is the trajectory of country X across institutions, rights,
  conflict, information and economy, against its own history and its region?" Served by the
  country profile.
- **Situation investigation.** "Courts in X are under pressure; what exactly happened, in what
  order, on what evidence, and what has happened elsewhere when this sequence appeared?" Served
  by the situation page with its evidence record, timeline and historical comparisons.
- **Source scrutiny.** "Who reported this, who else did, and are those reports independent?"
  Served by the evidence record and the source registry.
- **Coverage check.** "How well is region Y monitored at all?" Served by the coverage index,
  shown everywhere a country is shown.
- **Historical pattern study.** "How did episodes of judicial capture unfold, how long did they
  take, which ones were reversed, and by what?" Served by the episode library.

## 5. The eight questions

Every published assessment, and every event shown as significant, must answer in its first
screen: What happened? Where? When? Why is it relevant? How strong is the evidence? What is
changing? What historical context is useful? What should the reader investigate next? (START.md
section 9). The data model (document 08) stores each answer as a distinct field or relation so
the interface can never show one without the others.

## 6. Capabilities by maturity level

START.md section 13 names five levels that are not to be confused. Canary adopts them as named
milestones; the roadmap (document 10) maps phases to levels and says which level each phase
reaches. No phase claims a higher level than its acceptance tests demonstrate.

| Level | Meaning | Demonstrated by |
|---|---|---|
| L1 Visual prototype | The views exist with representative data | Screens render the eight questions; no claim about data |
| L2 Working dashboard with real data | Live ingestion from a small set of licensed sources, provenance intact | Every displayed item links to its raw document and source record; freshness shown |
| L3 Reliable multi-source monitoring | Many sources, health-checked; dedup and lineage; coverage index; corrections traceable | Ingestion survives source outages and API changes without silent gaps; lineage precision measured |
| L4 Historical and cross-domain analysis | Indicators with baselines, change detection, watch rules, episode library, comparison procedure | Worked situations with evidence records and comparisons; false-alarm review in place |
| L5 Validated early warning | Backtests without look-ahead show signals precede outcomes with stated precision and lead time | Published calibration log; external review |

The first public release targets L3 with parts of L4. L5 is a research goal, not a promise.

## 7. Non-goals

- No composite "threat score" per country, ever. The three layers (document 04) are shown side
  by side and never summed.
- No autonomous publication by a model. Every assessment is written or approved by a person.
- No full-text republication of articles or reports. Metadata, links, short excerpts and
  extracted claims with quoted spans only (note G-02).
- No scraping that ignores robots.txt, paywalls, or machine-readable reuse reservations.
- No requests for credentials, tokens, permissions or data access from any organisation; only
  sources usable without registration and with an explicit licence (document 03, section 8).
- No retention of article full text after processing; metadata, one short quoted span per claim
  and the extracted claim only. Open-licensed reports may be kept in full.
- No reader accounts beyond the Access allow-list; no personalisation; no tracking beyond
  aggregate, privacy-preserving analytics.
- No coverage of individuals' private lives. Actors are public officials, institutions,
  organisations and groups acting in public roles.
- No claim of equal coverage everywhere. The coverage index is always visible.

## 8. Constraints

- Hostname `canary.lucascosolo.com` on the user's Cloudflare zone, permanently behind
  Cloudflare Access with a friends allow-list (user input, 2026-10-20).
- Personal, non-commercial, published under the user's own name, no legal entity (user input,
  2026-10-20, afternoon). Source licences are evaluated for exactly that use; a public or
  commercial turn would require re-evaluation of the catalog (document 03).
- Legal exposure minimised by construction (document 04, section 9; document 07, section 5):
  open-licensed data only, short quotations only, conservative naming, honoured reuse
  reservations, a disclaimer and a corrections contact.
- One operator, developing with Claude Code, with compute on one workstation and light VPSes
  (machine context). The architecture must run on modest hardware and tolerate the operator
  being away for days.
- No `rm` anywhere, quarantine instead; no force-push; small commits (`AGENTS.md`).
- Budget: not yet stated by the user; the cost model in document 07 gives a floor and a
  comfortable level, and document 11 asks.

## 9. What makes Canary different

A news aggregator shows what was said. A risk dashboard shows a number. A geopolitical
intelligence platform shows an analyst's conclusion. Canary shows the claim, the quoted span, the
document, the source, the source's independence from the subject and from the other sources,
the count of independent lineages behind the claim, the contradicting evidence, the gaps, the
country's own baseline, the direction of change, the published base rate for the outcome
people fear, the historical episodes that resemble the situation and the ways they do not, and
the explicit conditions under which the assessment would be raised, lowered or withdrawn. It
does this for improvement as carefully as for deterioration, and it says where it cannot see.

## 10. Success criteria

For the first shared release (end of Phase 3 in document 10):

- Every item on the Today view answers the eight questions and links to raw evidence within two clicks.
- Every country page shows a coverage index, a freshness stamp per source, and an explicit
  "unknown" wherever data is missing, rather than a blank or a zero.
- Claim extraction meets the gold-set targets in document 09 for each language tier it is
  switched on for, and no claim is displayed without a quoted span that passes the support check.
- The lineage detector's precision on the test set is at or above the target in document 09,
  so "N independent lineages" is a number the reader can trust.
- A stable-period false-alarm review (document 09) has been run on at least ten country-years and
  its results published on the methodology page.
- At least twelve historical episodes are in the library with cited milestones, including at
  least four cases of reversal or resilience.
- A corrections log is visible to readers and every correction distinguishes source correction
  from Canary error.
- Every integrated source is usable without registration, has an explicit licence permitting
  storage and display for personal non-commercial use, and has its attribution text rendered
  where it requires it; everything else is a link.
- Monthly running cost is within the budget the user approves in document 11.
