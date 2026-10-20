# 05. Historical knowledge strategy

## 1. Purpose and the failure to avoid

The historical layer exists to answer "what has this looked like before, how long did it take,
what stopped it, and how is this case different", and to supply base rates. The failure START.md
warns against is the surface analogy: picking a famous catastrophe because it is salient and
matching on resemblance rather than mechanism. The research gives the method to avoid it:
Neustadt and May's procedure (list what is known, unknown and presumed; for each candidate
analogy list likenesses, differences and unclear; place institutions in their own history; draw
the time-line), Khong's finding that decision-makers choose analogies by recency and salience,
and the outside view (choose a reference class and start from its outcome distribution) (G-04).
Canary makes that procedure a required structure, not advice.

## 2. The episode library

An **episode** is a curated record of a bounded historical case. Records are hand-written in
versioned YAML with citations, reviewed, and loaded into the database; they are not generated.
Each episode has:

- identity: country, period (start and end dates, with precision), episode type (from a fixed
  list: executive aggrandizement, judicial capture, electoral manipulation, media capture,
  emergency-powers entrenchment, coup, self-coup, civil conflict onset, mass atrocity, territorial
  seizure, economic crisis with political effects, democratic transition, reversal/recovery,
  resilience/averted breakdown), the ERT or GWF code where one exists, and the outcome
  (breakdown, averted, reversed, ongoing at the record's date, other);
- a **time-line** of milestones: date, what happened, which institution or right, a claim-style
  record with sources (scholarship via OpenAlex, primary documents, datasets);
- **early signs**: which indicators moved first and when, with the lead time to the outcome;
  which developments at the time looked alarming and did not matter; what contemporary observers
  misread, with sources;
- **mechanisms**: the causal account the literature gives, with the competing accounts named;
- **protective factors** present or absent (judicial constraints, democratic stock, regional
  democracy, opposition strategy, civil-society density, military autonomy, economic conditions),
  drawing on Boese et al., Laebens and Lührmann, Gamboa, Straus (D-01, D-02);
- **duration** from first sign to outcome or reversal, and the sequence of steps;
- **what changed when it reversed**, for reversal and resilience cases;
- **comparability notes**: what in this case is tied to its period and place and does not
  travel (technology, international environment, regime type);
- sources and the reviewer.

Initial set (to be written in Phase 3; the list is a recommendation): Weimar Germany 1930-33;
Chile 1970-73; Argentina 1976; Rwanda 1990-94; Yugoslavia 1987-92; Venezuela 1999-2017; Hungary
2010-; Türkiye 2013-; Poland 2015-23 (with the 2023 reversal); Brazil 2019-23 (resilience);
Tunisia 2011-21 (transition then self-coup); Myanmar 2011-21; Sudan 2019-23; Benin 2007-12 and
South Korea 2008-17 (halted erosion, from Laebens and Lührmann); Malawi 2019-20 (court-annulled
election, resilience); The Gambia 2016-17 (peaceful transfer after refusal); Côte d'Ivoire and
Senegal in the 2000s (restraint, from Straus); Indonesia 1965-66; Cambodia 1975-79; the Soviet
purges 1936-38; apartheid South Africa and its transition. At least a third of the library must
be reversal, resilience or transition cases so that the comparison engine has the outside view's
full distribution to draw on.

## 3. Base rates and the outside view

Every comparison starts from a reference class and its outcome distribution, computed from the
datasets that allow it and quoted with their definitions: ERT episodes of autocratization and
their outcomes (V-Dem), the Boese et al. figure that 23% of completed episodes in democracies
averted breakdown (read in full, D-01), the V-Dem U-turn share (to verify against the primary
text before use, D-01), EWP's onset base rate of about 1% of countries a year (A-06), Cline Center
coup frequencies by decade (D-03). These are displayed as "of N episodes that began like this
in the reference class, M ended in breakdown, K reversed", with the dataset version. The
reference class and the counting rule are stated on screen.

## 4. The comparison procedure

A comparison is a structured record between a current situation and an episode. It is created by
the operator (with candidate suggestions from a deterministic matcher, section 5) and has:

- the situation's **known / unknown / presumed** lists at the time of writing;
- **likenesses**: specific, with the milestone in the episode and the claim in the situation;
- **differences**: same specificity, including institutional structure, regime type, regional
  environment, international constraints, technology, time period;
- **unclear**: what cannot yet be compared because the situation's data is missing;
- **placement**: a sentence placing the main actors and institutions in their own history;
- the episode's **time-line position**: which milestone of the episode the situation most
  resembles, and how long the episode took from there;
- the reference-class base rate (section 3);
- the required sentence, verbatim in every rendered comparison: "This comparison describes
  resemblance to a documented sequence; it is not a prediction. Episodes in the reference class
  ended in breakdown in M of N cases and were reversed in K."

Comparisons are versioned with the assessment they belong to and are retired when the
situation's facts change.

## 5. Candidate matching (deterministic, assistive)

To suggest episodes worth comparing, Canary matches on structured features, not text: episode
type, the set of institutions affected, the order of the first three milestones, the regime type
and baseline quartiles at onset, and the presence or absence of protective factors. The matcher
is a published scoring of feature overlap (a count, shown as "shares 4 of 7 structural features"),
and it exists only to surface candidates to the operator. No language-model similarity, no
embedding of narratives, no automated publication of a comparison (START.md section 4 asks for
exactly this discipline). To validate: in Phase 4, hide the outcome of half the library's episodes
and check whether the matcher's top candidates for a known episode's early milestones include
cases with the same and with different outcomes; a matcher that only returns catastrophes fails.

## 6. Representation

Episodes, milestones, mechanisms and comparisons are relational records in the same database as
the rest of Canary (document 08), with Wikidata identifiers for actors and places so that an
episode's institutions link to today's. A graph database is not needed: the relationships are
few and shallow (episode has milestones; milestone cites documents; comparison links situation
to episode) and recursive SQL covers the one traversal (chains of related episodes). SEM, LODE
and CIDOC-CRM were reviewed (G-04); Canary borrows their event-with-time-and-place-and-actor
shape without adopting an RDF stack. Export of the library as JSON-LD under CC BY-SA (inheriting
V-Dem's ERT where used) is a Phase 4 deliverable so that others can reuse it.

## 7. Validation of the historical layer

- Every milestone has at least one citation a reader can open; a milestone without one is
  shown as a draft and excluded from matching.
- A second reviewer (or a later session with the adversarial checklist) reads each episode for
  the "what observers misread" and "differences that do not travel" sections before it is
  published; these are the sections that prevent sensationalism.
- The matcher test in section 5.
- A yearly re-read of each episode against new scholarship (OpenAlex query by episode keywords),
  logged in the episode record.
- The calibration log (document 09) records every comparison that, in hindsight, pointed the
  wrong way, with the reason, so the library's "what observers misread" grows with Canary's own
  misreadings.
