# 09. Validation and testing strategy

The principle from START.md section 12: a system that looks impressive but misses developments,
raises false alarms, or invents parallels has failed. Validation therefore runs at three levels
(code, data, analysis) and the analytical results are published, including the bad ones.

## 1. Code: unit and integration

Every adapter has fixture-based tests (recorded responses, never live calls in the suite) for
`discover`, `fetch`, `parse` and `health`, including a schema-change fixture that must raise a
health alert rather than produce silent garbage. Normalisation, lineage clustering, indicator
computation, baselines, change detection, rule evaluation and the coverage index each have
deterministic tests on small fixtures with known answers. The reproducibility test re-runs each
stage on a fixture with pinned versions and asserts byte-identical outputs. API tests check
that every public resource carries licence and attribution and that `licence_mode` is honoured
by the renderer. Tests write JUnit XML and the suite's `output-triage` reads the report (suite
rule). Tests that exercise deletion or moves use temporary directories only (suite rule).

## 2. Data quality

Nightly checks, each a calibration-log entry when it fails: freshness per source against its
declared lag; duplicate rate after lineage clustering; geocoding accuracy on a rolling random
sample of 50 claims a week hand-checked by the operator; language-identification accuracy on
the same sample; vintage integrity (no observation without a release); observation outliers
against the source's own documented range; claim-type distribution drift per source (a sudden
shift is either news or a broken parser, and the operator decides which).

## 3. Extraction validation (the measurement instrument)

A **gold set** of hand-coded documents is built before extraction is switched on for a
language tier: at least 300 documents for English, 150 each for the next tier (Spanish, French,
Arabic, Russian, Portuguese, to be confirmed against the feed list), 100 for each further
language, stratified by source class and domain, coded by the operator with the codebook and a
second pass for a 20% subsample to measure inter-coder agreement (reported, not hidden). For
each model version and prompt version, report per claim type: precision, recall, F1 for claim
presence; accuracy for actor class, target class, place, time; span fidelity (the quoted span
exists verbatim and supports the claim, judged by hand); the codebook-following check from He
et al. 2026, that is, agreement after label definitions are re-mapped, so that a model that
scores well for the wrong reasons is caught (F-05). Targets for switching a tier on: F1 at or
above 0.75 for the institutional and conflict claim types, span fidelity at or above 0.95, and
no claim type with precision below 0.6 displayed (those are extracted but held for review).
Targets are revised from measurements, with the revision logged. Re-validation is mandatory on
any model or prompt change and every quarter against drift.

## 4. Lineage and independence

A hand-labelled set of 500 document pairs (same story, different outlets; wire copy with and
without attribution; press-release churn; genuinely independent reports on the same event)
measures clustering precision and recall and the attribution parser's accuracy. Target: precision
at or above 0.9 (a false merge understates evidence; a false split overstates it, and
overstatement is the worse error for a warning system, so precision is weighted). The number
"K independent lineages" is shown with a tooltip stating the measured precision of the method
version that produced it.

## 5. Backtesting without look-ahead

The hard rule, from the economics real-time-data practice and the ViEWS competition design (G-03,
D-03): a signal or rule is evaluated only against what was knowable on the date it would have
fired. Canary's observations keep vintages (document 08) so index-based signals can be replayed
honestly; for news-based signals the replay uses GDELT's timestamps and Media Cloud's story dates
for discovery, with documents fetched from the Internet Archive capture nearest the date where
the live page has changed. Any backtest that cannot reconstruct the information set says so and
is labelled "hindsight-assisted", a separate category.

Test cases: twelve episodes from the library with known outcomes (six deterioration, three
reversal, three stable-but-dangerous) and ten stable country-years from countries with high
coverage, all from 2015 onward so that the news sources exist. For each watch rule and each
change-detection method, report: probability of detection (did it fire before the outcome),
lead time distribution, false-alarm ratio on the stable set and on the reversal cases, and the
precision-recall curve where a threshold exists; never accuracy, for the reason the coup
forecasts show (AUC-ROC about 0.8 with AUC-PR 0.02 to 0.05; D-03). Report against base rates
from ERT and the Cline coups. A rule that does not beat a trivial baseline (fire on any
deterioration claim) on precision at the same recall is not enabled.

## 6. Bias and symmetry tests

- **Ideological symmetry**: matched pairs of situations under governments of opposite
  orientation with comparable claim sets; the rules must fire or not fire identically; the
  operator's assessment language is checked by a second pass for asymmetric phrasing.
- **Geographic consistency**: the same claim type with the same evidence profile in a
  high-coverage and a low-coverage country must receive the same confidence inputs, with the
  coverage label carrying the difference, not the confidence.
- **Source-class ablation**: drop each source class (wire, NGO, official) from the input and
  measure how many assessments lose their evidence floor; assessments that depend on one class
  are labelled as such.
- **Reporting-suppression test**: inject synthetic shutdown periods into the replay and confirm
  that volume signals are suppressed and the "reporting may be suppressed" note is attached.

## 7. Editorial review checklist (before publishing a strong assessment)

Required for direction "deteriorating" at confidence "high" or above, for any assessment naming
a UN Framework factor, and for every first assessment of a new situation: the evidence record
has at least two independent lineages per load-bearing claim or says why not; contradicting
evidence has been searched for and recorded, including the official position; the best
alternative explanation is written down with the evidence that would distinguish it (an
adversarial draft from the model is allowed as input); the comparison records have their
differences section filled; the three "what would change this" conditions are concrete and
observable; no prohibited phrase is present; the confidence inputs are set and the severity is
in words; a source whose terms are "unverified" is cited by link only. The checklist completion
is stored with the assessment version.

## 8. Security testing

A corpus of prompt-injection documents (instructions to the extractor hidden in article bodies,
in metadata, in PDF layers; adversarial claims that quote themselves) is part of the extraction
test suite; the pass condition is that no claim without a verbatim span passes, no instruction
changes the output schema, and nothing in the document reaches the drafting model. The
harness's `/security-review` runs on each completed module. Dependency audit monthly. A
quarterly restore drill from the storage VPS backup is an acceptance item for Phase 2.

## 9. Performance and experience

Budgets: Today first screen under 150 KB and under 1.5 s server render on the target host;
country page under 2.5 s; API p95 under 500 ms for cached resources. Load test at the edge
before public launch. Accessibility audit (keyboard-only pass of every view; screen-reader pass
of Today and a situation page; contrast check in both themes). A small reader test (five
people, three of them unfamiliar with the domain) before launch: can they find the evidence
behind an item in under a minute, and do they correctly read the confidence and coverage
labels? Their misreadings become copy changes.

## 10. The public calibration log

Every false alarm (a flag or assessment that later proved unfounded), every miss (an outcome in
a monitored country with no prior situation), every late warning, every retired rule, every
backtest result and every comparison that pointed the wrong way is an entry with a date, the
item, and what was learned. The log is public from the first public release. Its first entries
are the backtest results from Phase 4 and the stable-period false-alarm review, which is run
before any watch rule is enabled.

## 11. External review

Before public launch and yearly after: an invited read of the framework, the rule set and a
sample of assessments by two or three people with domain standing (comparative politics,
atrocity prevention, OSINT verification), with their comments published alongside the response.
Not a gate on publishing (suite rule: a second opinion is a tool, not a gate), but a recorded
input.
