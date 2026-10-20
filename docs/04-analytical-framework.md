# 04. Analytical framework

This is the part of Canary that has to be right before anything is built on it. It takes the
structure of the problem from the research (document 02) and turns it into rules that code can
implement and readers can audit. Everything here is a recommendation; the places where a rule
needs an experiment before it is fixed are marked "to validate" and appear again in document 09.

## 1. Three layers that are never summed

Canary keeps three kinds of statement apart and shows them side by side:

1. **Baseline (level).** Where a country stands on slow-moving, externally produced measures:
   V-Dem's indices with their confidence intervals, Freedom House, the EWP structural risk
   assessment with its base rate, WGI, press-freedom and civic-space ratings, macro context.
   Annual or slower. The question it answers: "how much institutional margin does this country
   have, and what do established models say about its structural risk?"
2. **Change (signals).** What moved recently, relative to the country's own history: indicator
   series with change-point and exceedance detection, event streams (UCDP, extracted claims),
   attention volume (GDELT) normalised for reporting capacity, and information-control events.
   Daily to monthly. The question: "is something departing from this country's normal?"
3. **Assessment (judgement).** A human-written or human-approved statement about a situation,
   with an evidence record, a confidence label, a direction, the historical comparisons, and the
   conditions that would change it. The question: "what do we make of it, and how sure are we?"

A reader sees all three for any country or situation, each labelled with what it is. There is no
fourth number that combines them. A country with a weak baseline and no change signal is shown
as "structurally exposed, stable"; a country with a strong baseline and several converging change
signals is shown as "resilient baseline, deteriorating"; both are flagged for different reasons,
in words, never on one scale (START.md section 7 asks for exactly this distinction).

## 2. Claims and evidence records

The unit of evidence is the **claim**: a statement extracted from one document, carrying the
quoted span that supports it, the document, the source, the actor, the target, the place, the
time, a claim type from Canary's vocabulary, and the extraction run that produced it. A claim is
never shown without its quoted span and its document link.

The unit of judgement is the **evidence record** attached to an assessment or to an event. It
lists, as separate fields that are never merged:

- claims that support, claims that contradict, and claims that qualify;
- for each claim, the source's class and its independence from the subject (is the source the
  government being assessed, an opposition party, a party to the conflict, a funder of one side,
  a wire service, a local outlet, an NGO that advocates on the issue, an intergovernmental body);
- the number of **independent lineages** behind the supporting claims (section 3), not the number
  of documents;
- the evidence category of each item, from START.md section 6, as an enumerated field:
  `documented_fact`, `official_claim`, `independent_report`, `corroborated_allegation`,
  `uncorroborated_allegation`, `expert_interpretation`, `statistical_finding`,
  `historical_comparison`, `model_hypothesis`, `forecast`, `legal_finding`, `unknown_or_disputed`;
- the process-tracing weight of the item for the conclusion, in Bennett and Checkel's terms
  (`straw_in_the_wind`, `hoop`, `smoking_gun`, `doubly_decisive`), chosen by the reviewer (G-04);
- what is missing: the specific documents or confirmations that would be expected if the claim
  were true and have not been found, written as text;
- the reviewer, the date, and the version.

The evidence record is what the "How strong is the evidence?" panel renders (document 06).

## 3. Source independence and lineages

Five articles repeating one ministry statement are one piece of evidence. Canary therefore
clusters documents into **lineages** before counting anything:

1. Near-duplicate detection on extracted text with shingling and MinHash (datasketch), tuned on a
   hand-labelled set (document 09): documents above the similarity threshold share a lineage.
2. Attribution parsing: bylines and body phrases that name a wire service, a press release, an
   official statement or another outlet ("according to", "reported by", "said in a statement")
   assign the document to the lineage of the named origin, even when the text differs.
3. Quoted-statement matching: claims whose quoted span is the same statement (same speaker, same
   wording after normalisation) share a lineage.
4. Everything else is its own lineage.

A lineage carries an `origin_class` (official statement, wire, single outlet, NGO report, court
document, dataset) and the earliest document seen. The evidence record counts lineages by origin
class. Two lineages count as independent corroboration only when their origins are different
sources that are not both parties to the matter being assessed. To validate: lineage precision
and recall on the test set (document 09, section 4).

Reporting volume is always read against capacity. For each country Canary maintains a
**coverage index** (section 6); a rise in attention in a country with high coverage and no
shutdown is a different signal from the same rise in a country where three outlets exist and
OONI shows blocking. When coverage drops (outages, shutdowns, outlet closures) the system adds a
"reporting may be suppressed" note to every change signal for that country rather than reading
silence as calm. START.md's rule that missing information is never evidence that nothing
happened is implemented as a hard constraint: an indicator with no observation in its expected
window is displayed as "no data" with the date of the last observation, never as zero.

## 4. Grading sources without one number

Each source in the registry carries separate, declared attributes (document 03, section 7):
type, class, independence from subjects, ownership and state control, revision policy, and free
text on known biases with citations. Canary publishes no composite reliability score, because
the research found no defensible global one (G-01) and because a single number hides exactly
the distinctions START.md section 6 wants kept. Per claim, the reviewer records the Admiralty-style
pair as two fields: source reliability for this kind of claim (`A` to `F`) and information
credibility for this claim (`1` to `6`) (C-03). The pair is shown as two words, never as a product.

Rules that apply symmetrically to every government, party and movement:

- An official denial is recorded as an `official_claim` on the contradicting side, with its
  source class; it does not cancel independent evidence and it is not ignored.
- A source is not downgraded for criticising a powerful actor and not upgraded for being
  Western, institutional or centrist; only its documented record, independence and access
  matter, and those are written down, not scored.
- Advocacy organisations' reports are `independent_report` or `corroborated_allegation`
  depending on their own stated methodology for that report, and the registry entry says
  what the organisation advocates for.

## 5. Indicators, baselines and change detection

An **indicator** is a defined series with: a definition, the source and its licence, cadence,
units, the direction that counts as deterioration, the baseline method, the change-detection
method and its parameters, and a text caveat on reporting bias. The catalog of indicators is a
versioned file; every signal names the indicator version that produced it.

Baselines are per country, from the country's own history, with three horizons: the last twelve
months, the last five years, and the full available series. Change detection runs, by
indicator type:

- for counts and volumes (events, attention, shutdown events): an expected-count model with
  trend and seasonality (the Farrington family or a simpler quasi-Poisson regression) and an
  exceedance threshold; the threshold is chosen by historical noise-to-signal ratio on the
  backtest set in the way the financial signals approach does (C-02), and the chosen window is
  declared (to validate: document 09);
- for annual indices (V-Dem, FH): year-on-year change beyond the index's own confidence interval,
  and the ERT-style rule for an episode (a cumulative decline past a stated threshold over a
  stated window), using V-Dem's own definitions where they exist;
- for slow macro series: change-point detection (PELT via `ruptures`, or a vendored
  implementation if the library goes unmaintained; F-02) with a minimum segment length;
- for event sequences: rule-based detection of ordered patterns within a window (section 7).

Every signal records: indicator, country, window, method and version, the statistic, the
threshold, the baseline values, and the coverage index at the time. Signals are automated and
labelled as such wherever shown. They are inputs to review, not published conclusions.

## 6. The coverage index

For each country and month, Canary computes and displays:

- the number of active registered sources that cover the country, by source class and language;
- the baseline document volume per day over the last year and the current volume;
- whether an information-control event is active (Cloudflare Radar, OONI, #KeepItOn);
- the share of integrated indicators that have a current observation;
- the most recent human review of the country's situations.

These are shown as five separate facts, with a one-word summary (high, medium, low, obscured)
derived by a published rule. The summary is a label on every country reference in the interface.
A global map that is "well covered in Europe and poorly in the Sahel" says so on the map.

## 7. Watch rules: convergence without arithmetic

START.md asks how to recognise combinations that matter more together than apart without
assigning points. Canary does it with **watch rules**: human-written, versioned, published rules
in a declarative file that produce a named **flag** when their conditions are met. A rule has
a name, a rationale with citations, a scope (which countries or regime types it applies to), a
window, conditions expressed over signals, claims and baseline values, a required evidence
quality, and the text of what would strengthen, weaken or withdraw the flag. A rule never
multiplies or adds; it tests conditions. Examples of the form (the exact thresholds are to be
set in Phase 2 and validated in Phase 4):

- `institutional_convergence_90d`: within 90 days, claims of type `judicial_independence_attack`
  and at least two of {`opposition_restriction`, `emergency_powers_expansion`,
  `media_pressure_state`, `election_administration_attack`} each supported by at least two
  independent lineages, in a country whose V-Dem judicial-constraints index is above the global
  median (so that the baseline says this is a departure). Strengthened by: a court ruling
  against the measure being ignored. Weakened by: a court blocking the measure and the
  government complying. Withdrawn by: reversal of two of the measures.
- `reporting_suppression`: an information-control event is active and document volume has
  fallen by more than the exceedance threshold; the flag's text is "reporting may be
  suppressed; absence of events is not evidence". It attaches to every other flag for the
  country while active.
- `recovery_candidate`: a previously flagged situation where the triggering measures have been
  reversed or struck down and no new ones have appeared for the window; produces a flag whose
  direction is improvement, reviewed with the same rigour.

Flags go to the operator's review queue. A flag is public only inside the country or situation
page, in a section labelled "automated flags, not yet reviewed", below reviewed assessments. A
reviewed flag becomes, or updates, an assessment.

The rule file and every change to it are in version control; the methodology page lists the
rules in force with their rationale. Rules are tested against historical episodes and stable
periods before they are switched on (document 09), and their false-alarm count is part of the
public calibration log.

## 8. Assessments and confidence language

An assessment is written about a **situation** (a country plus a theme, for example "Judicial
independence in X"). It has a required structure that maps to the eight questions:

1. What happened (one paragraph, claims linked).
2. Where and when (place and period; structured).
3. Why it matters (the mechanism: which institution or right is affected, and how this fits the
   backsliding or escalation sequences documented in the literature, with citations).
4. Evidence (the evidence record, section 2).
5. What is changing (direction: deteriorating, improving, stable-but-dangerous, mixed; the
   signals and the baseline it is measured against).
6. Historical context (comparisons from the episode library, document 05, each with its
   likenesses, differences and unclears, and the sentence "this is not a prediction").
7. What to investigate next (open questions, missing evidence, upcoming scheduled events such
   as a court date or an election).
8. What would change this assessment (explicit conditions for raising, lowering, withdrawing).

Confidence follows the IPCC two-axis scheme (C-03): the reviewer records the **amount of
evidence** (limited, medium, robust) and the **agreement among independent sources** (low,
medium, high); the displayed confidence (very low to very high) is derived from the two by a
published table and both inputs are shown next to it. Likelihood words (ICD 203 bands) appear
only when an assessment quotes a published model's probability and then the model, its base rate
and its stated precision are quoted with it; an assessment never states a probability of its own.
A likelihood word and a confidence level never share a sentence (ICD 203 rule, C-03). Phrases
like "on the brink", "imminent" and "inevitable" are prohibited in assessment text by the style
guide, and the review checklist enforces it.

Severity is a separate field in words: what is at stake if the trend continues (loss of a
specific right, closure of a specific institution, risk to a specific population), tied to the
UN Framework risk factors where a mass-atrocity concern exists (A-06), not a number.

## 9. Required review before strong statements

The research on HealthMap (every report curated daily by staff, C-02) and on LLM extraction
error (F-05) settles the workflow: automation proposes, people publish. Concretely:

- claims are extracted automatically, pass a deterministic schema check and a support check
  (does the quoted span exist in the document and entail the claim, scored by a second,
  cheaper model pass and spot-checked by hand), and are then visible as claims with their
  extraction run labelled;
- events are assembled from claims by rules and by the operator; an event with fewer than two
  independent lineages is labelled "single-sourced";
- assessments are written by the operator (Claude may draft, with every sentence tied to a
  claim identifier, and the draft is labelled as such until a person approves it);
- an assessment whose direction is "deteriorating" with confidence "high" or above, or that
  names an atrocity-risk factor, requires the review checklist (document 09, section 7),
  including an adversarial pass that lists the best alternative explanations and the evidence
  that would distinguish them, before it is published;
- disagreements among reputable sources are recorded as such in the evidence record and shown
  to readers; Canary does not resolve them by majority;
- naming is conservative (user decision of 2026-10-20, afternoon): assessments name
  institutions, offices and organisations; a person is named only in official capacity and only
  for a documented official act (a decree, a ruling, a vote, a public statement with the quote
  and its source); allegations about a person's conduct beyond documented official acts are not
  published in Canary's words and are at most linked to the reporting source with its evidence
  category shown; every assessment is phrased as an opinion based on the disclosed, cited facts
  on the same screen.

## 10. Worked examples (hypothetical)

**Example A: convergence in a country with strong courts.** Over ten weeks, country X's
parliament passes a law changing the appointment of supreme-court judges; two opposition
candidates are barred by the election commission; a state of emergency is extended for the
third time; the public broadcaster's board is replaced. Claims arrive from local outlets, two
wire services, an NGO report and a government press release. Lineage clustering shows the
appointment law and the broadcaster change each have three independent lineages (local
outlet, wire, NGO); the candidate bar has two (wire and the commission's own statement, which
is an `official_claim`); the emergency extension has one lineage plus the decree itself, a
`documented_fact`. The baseline shows X in the top quartile of V-Dem judicial constraints. The
`institutional_convergence_90d` rule fires. The operator reviews: amount of evidence robust,
agreement high, confidence high; direction deteriorating; severity "independence of the highest
court and the fairness of the next election"; historical comparisons from the library (say,
two episodes of court-packing followed by breakdown and one followed by reversal after a
court-and-street response), with differences (X has a federal structure and an independent
election observer presence); what would change it: "the constitutional court strikes down the
appointment law and the government complies (lower); the court is itself reconstituted
(raise); the barred candidates are reinstated on appeal (lower)". Published with all of that visible.

**Example B: the same events in a country with weak courts.** Country Y has the same sequence,
but Y is in the bottom quartile of judicial constraints and has had two prior episodes. The
baseline already says "structurally exposed". The rule's scope clause means the convergence flag
still fires, but the assessment's "why it matters" is different: this is persistence or
intensification, not departure, and the historical comparisons are to consolidation episodes, not
onset episodes. The interface shows Y under "ongoing" rather than "new".

**Example C: a reporting spike.** Attention volume for country Z triples in a week. The coverage
index shows a new international story (a visiting head of state) and no new claims of the
institutional types; UCDP shows nothing; OONI shows no blocking. The volume signal fires, no
watch rule does, and the automated flags section says "attention rose; no corresponding
institutional, rights or conflict signals". No assessment is written. The signal is logged for
the false-alarm review.

**Example D: improvement.** In country W, a previously flagged situation (media pressure) sees
the regulator's order struck down, the broadcaster's licence restored and the responsible
minister replaced; two independent lineages for each. The `recovery_candidate` rule fires. The
assessment's direction becomes "improving", confidence medium (amount medium, agreement high),
with the comparison to episodes where reversal held and where it did not, and "what would change
this": "a new licensing order (raise concern again); six months without further measures (close
the situation)". The Today view shows improvement with the same prominence it gave the
deterioration.

**Example E: not enough to say.** Reports from one diaspora outlet allege mass arrests in a
region of country V during a shutdown. One lineage, `uncorroborated_allegation`, coverage
"obscured". The evidence record says what is missing (any second lineage; satellite imagery of
detention sites; a UN or NGO statement) and the situation is published as "unverified reports
during a reporting blackout; investigation open" with confidence very low. Canary does not
dismiss it and does not amplify it.

## 11. What is deliberately not in the framework

No country probability of breakdown, coup, war or atrocity. No learned model that maps indicators
to outcomes until a backtest without look-ahead (document 09) shows that it beats the published
models and the simple rules on precision at a stated lead time. No sentiment scores of political
speech as evidence of anything (START.md section 3F); rhetoric is tracked only as claims of
specific speech acts (an official calling a group a named dehumanising term, on a date, with
the quote), which the UN Framework treats as an indicator of its factor 10. No automated
historical analogy by text similarity (document 05).
