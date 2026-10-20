# G-04: Methods for historical analogy and comparison; structured regime-episode datasets; knowledge representation

- Date: 2026-10-20
- Agent: researcher (Sonnet, low effort), 12 tool uses
- Status: sections 1-2 are the agent's recall of the works, not re-read; section 3-4 partly fetched.

## Answer (verbatim; read 2026-10-20)

1. Analogy methods (from memory, unverified this session).
- Neustadt & May 1986 (Free Press): list Knowns / Unknowns / Presumed, then for each candidate analogy list Likenesses, Differences and Unclear. Goldberg rule: ask "what's the story?" before "what's the problem?". Placement: put people and institutions in their own history. Time-lines: chart the issue's trajectory.
- Khong 1992 (Princeton UP): the AE framework has analogies perform diagnostic tasks (classify the situation, assess stakes, prescribe, predict, judge morality, warn of risks). Leaders pick analogies from salient, recent, personally experienced events, so test the match on causal structure, not surface similarity.
- May 1973 (Oxford UP): policymakers grab the most recent or vivid precedent and rarely test it. Ask whether the precedent really fits, and look for several.
- Brändström, Bynander & 't Hart 2004 (Public Administration 82(1)): crisis managers use history both to decide and to justify. Record who invokes which analogy and for what purpose.
- Kahneman & Lovallo 1993 / Flyvbjerg: take the outside view. Choose a reference class, use its outcome distribution as the baseline, and adjust only for case-specific evidence.

2. Comparative methods (from memory, unverified this session).
- George & Bennett 2005 (MIT Press): structured, focused comparison. Ask the same theory-derived questions of every case, and cover only the variables that matter.
- Bennett & Checkel 2015 (Cambridge UP): process-tracing tests. Straw-in-the-wind is weakly informative either way. Hoop is necessary but not sufficient, so failing it eliminates the hypothesis. Smoking-gun is sufficient but not necessary. Doubly decisive is both.
- Ragin's QCA (1987, 2000) uses set theory and Boolean logic to find the combinations of conditions that are necessary or sufficient for an outcome.

3. Datasets (fetched where noted).
- V-Dem ERT: https://github.com/vdeminstitute/ERT. The R package has `get_eps`, `find_overlap`, `plot_episodes` and `plot_all`. v16.0 is built on V-Dem v16, and the data is also offered as CSV or xlsx. Variable names, coverage years and license were not found; the codebook is at https://github.com/vdeminstitute/ERT/blob/master/inst/ERT_codebook_v16.pdf (not read).
- GWF: https://sites.psu.edu/dictators/. Two files, "Autocratic regimes" and "All political regimes", come in one ZIP with a PDF codebook. Fields are regime start and end dates, regime type, failure event category and violence level. The citation is Geddes, Wright & Frantz 2014, Perspectives on Politics 12(2). The 1946-2010 coverage is your figure; the page does not state it. License not found.
- Boix-Miller-Rosato: Harvard Dataverse page returned empty. Coverage, URL and license not found.
- Archigos: https://www.rochester.edu/college/faculty/hgoemans/data.htm. Version 4.1 runs through 2015 and is a Stata .dta file with PDF case descriptions. Version 2.9 covers 1875-2004. Election dates are CSV. License not found.
- Cline Center, Powell-Thyne, Svolik, Historical V-Dem: not checked.
- COW: https://correlatesofwar.org/data-sets/. War data 1816-2007 (v4.0; intra-state v5.1), MID 1816-2014, and other series. Terms: non-commercial use only, no redistribution without written permission, cite each dataset. This conflicts with an open knowledge base that redistributes data.

4. Knowledge representation.
- CIDOC CRM: https://www.cidoc-crm.org/. It is the ISO 21127:2023 ontology for cultural-heritage information integration. License not found.
- SEM and LODE: not read. The SEM page had an expired certificate, and LODE was not attempted.
- Wikidata P793 (significant event): https://www.wikidata.org/wiki/Property:P793. Values are items and must carry date and context qualifiers. Constraints limit the value types. I did not check its historical coverage.
- Seshat: https://seshat-db.com/. It lists 864 polities across 47 regions and 10 macro regions. Variable sets are social complexity, warfare, religion and economy, plus CrisisDB. It links to downloads, an API and GitHub. The license is on its "User Agreement & Data License" page, which I did not read.

## Evidence

- https://github.com/vdeminstitute/ERT — functions and the v16 version; no variable names
- https://sites.psu.edu/dictators/ — GWF contents and citation
- https://www.rochester.edu/college/faculty/hgoemans/data.htm — Archigos versions and formats
- https://correlatesofwar.org/data-sets/ — COW coverage and terms
- https://seshat-db.com/ — Seshat coverage
- https://www.wikidata.org/wiki/Property:P793 — P793 usage rules
- https://www.cidoc-crm.org/ — ISO 21127:2023

## Caveats (verbatim)

Sections 1 and 2 are unverified recall. Publisher pages are still to be read. Not found: ERT variables and license, BMR, GWF license, Archigos license, Seshat license, SEM and LODE, Cline Center, Powell-Thyne, Svolik, Historical V-Dem.

## Orchestrator note

The Neustadt-May procedure (Known/Unknown/Presumed; Likenesses/Differences/Unclear; placement; time-lines) and Khong's warning that analogies are chosen by salience rather than causal structure are adopted as the written procedure for every historical comparison Canary publishes (`docs/05`). The process-tracing test vocabulary (hoop, smoking-gun) is adopted for the evidence records that support an assessment. ERT (CC BY-SA via V-Dem) is the backbone episode list; COW's no-redistribution terms keep it out of the public knowledge base.
