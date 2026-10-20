# D-03: Conflict forecasting literature 2017-2025, coup datasets, coup forecasting

- Date: 2026-10-20
- Agent: researcher (Sonnet, low effort), 21 tool uses

## Answer (verbatim; read 2026-10-20; many publisher pages returned 403, so several items rest on abstracts or catalog records, not full text)

1. Cederman & Weidmann 2017, Science 355(6324):474-476, doi 10.1126/science.aal4483. Risk maps are feasible, but whether and when conflict breaks out in a given place is almost impossible to predict (authors' ETH interview). The "persistence drives accuracy" point is my recollection and was not confirmed from the text.
2. Hegre, Metternich, Nygård, Wucherpfennig 2017, JPR 54(2):113-124, doi 10.1177/0022343317691330 (open access). Forecasting means predicting unrealized outcomes from models estimated on realized data. The issue shows current approaches can forecast, and it asks for theory, interpretability, replicability and data collection. The out-of-sample/temporal-split standard was not confirmed in the abstract.
3. Chadefaux 2017, Data Science 1(1-2), doi 10.3233/DS-170002 (the DOI form in the URL I read; his TCD profile says 2018). He asks whether forecast failures are fixable model/data limits or fundamentally unpredictable features of conflict, and proposes research to separate the two. His specific limits are not found.
4. Mueller & Rauh 2022, JEEA 20(6):2440-2467, doi 10.1093/jeea/jvac025. Onsets in previously peaceful countries are rare and hard to predict. They topic-model about 4M newspaper articles and feed a random forest. The CEPR working paper (DP13748, 2019) says forecasting the hard cases is possible and benefits from supervised learning. Not read: the APSR 2018 paper, so what topics add over structural data there is not found. conflictforecast.org (read at conflictforecast.org; the www host fails TLS) shows a 12-month risk map for countries without conflict and an intensity forecast for those in conflict. Cadence, license and downloads: not stated.
5. Blair & Sambanis 2020, JCR 64(10):1885-1915, claim their theory-driven escalation model does as well as or better than atheoretical ML. Beger, Morgan & Ward (2021) argued it underperforms inductive alternatives. Blair & Sambanis, "Is Theory Useful for Conflict Prediction?", JCR 65(7-8):1427-1453 (2021), say the dispute hinges on smoothed versus empirical ROC curves. The dispute is unresolved by consensus, and I did not read the Beger et al. text.
6. Hegre, Vesco et al. (74 authors), JPR 62(6):2070-2087 (2025), doi 10.1177/00223433241300862; preprint arXiv 2407.11045 (doi 10.48550/arXiv.2407.11045). Teams forecast UCDP fatalities as 15-1000 samples per country-month or PRIO-GRID-month (Parquet), and CRPS is the main ranking score, with ignorance and mean interval score secondary. There were 13 teams and 23-24 models. The preprint reports benchmarks only: country-month CRPS was 49.4 for the 12-month "conflictology" benchmark, 56.8 for all-zero and 158 for last-value. Contributor results come in a later evaluation article, not found.
7. Powell & Thyne 2011, JPR 48(2). The maintained page is https://www.uky.edu/~clthyn2/coup_data/home.htm (.txt files, unverified; fetch failed on TLS). Format, last update and license: not found. Jonathan Powell's page returned 404. Cline Center Coup d'État Project: v2.1.3 (Feb 2024) covers 1945-2023, with 1000 events (443 coups, 352 attempts, 205 conspiracies) and a CSV of 29 variables. v2.2.0 (Jan 2025) added 94 events. v2.2.2 (Feb 2026) has 1,161 events, 1945 to early 2026. It is hosted on Illinois Data Bank (v2.2.2 DOI 10.13012/B2IDB-9651987_V10), and the listings say CC BY. Sahel: the OECD paper by Thurston finds the 2020-23 juntas' policies worsened violence beyond the pre-coup trend. The Mo Ibrahim 2023 report treats the wave as contagion, preceded by governance deterioration. No formal "coup belt" academic paper was found.
8. Predictive Heuristics (Beger, Ulfelder lineage): random-forest coup forecasts for 2010-2019 had AUC-ROC about 0.78-0.81 but AUC-PR only 0.02-0.05 (under 4% of country-years have an attempt). No peer-reviewed accuracy figure found.

## Evidence

- https://www.prio.org/publications/10468 and https://ideas.repec.org/a/sae/joupea/v54y2017i2p113-124.html — Hegre et al. abstract
- https://journals.sagepub.com/doi/full/10.3233/DS-170002 — Chadefaux
- https://www.futurity.org/?p=1353312 — Cederman & Weidmann interview
- https://bse.eu/research/publications/hard-problem-prediction-conflict-prevention — Mueller & Rauh abstract
- https://conflictforecast.org/ — the live forecast page
- https://arxiv.org/html/2407.11045v1 — challenge design and benchmarks
- https://www.prio.org/publications/14414 — JPR record
- https://databank.illinois.edu/datasets/IDB-8026876 — Cline v2.1.3 record
- https://clinecenter.illinois.edu/node/46 — Cline project page
- https://www.oecd.org/en/publications/military-coups-jihadism-and-insecurity-in-the-central-sahel_522f69f1-en.html
- https://www.predictiveheuristics.com/forecasts/about.html

## Caveats (verbatim)

Science, SAGE and Illinois Data Bank pages returned 403, and the Thyne page failed TLS. Items 1, 4-5 and 8 come from search-result summaries, not the papers. The Blair & Sambanis 2020 and Mueller & Rauh APSR 2018 DOIs were not verified. Powell & Thyne 2011 and the Beger et al. reply were not read.

## Orchestrator note

The coup-forecast figures (AUC-ROC about 0.8, AUC-PR 0.02-0.05) are the clearest statement of the rare-event problem: a model can rank countries well and still be wrong almost every time it flags one. Canary's warnings must therefore be framed as "attention and evidence", never as event probabilities, unless a published model with a published precision is being quoted. The Cline Center coup dataset (CC BY, updated to early 2026) is a usable live outcome series for backtesting coup-related indicators.
