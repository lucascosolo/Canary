# G-03: Scoring rules for rare events, human calibration, temporal validation, forecasting platforms, published EW evaluations

- Date: 2026-10-20
- Agent: researcher (Sonnet, low effort), 17 tool uses

## Answer (verbatim; read 2026-10-20; items marked [recall] were NOT verified this session)

1. Scoring. Saito & Rehmsmeier, PLoS ONE 10(3):e0118432, published 4 Mar 2015 (read): ROC plots can mislead on strongly imbalanced data because specificity hides a flood of false positives. PRC plots show the share of true positives among predicted positives, and the authors recommend them as "the most informative" tool. Gneiting & Raftery 2007, JASA 102(477):359-378: a rule is strictly proper if the expected score is uniquely optimised by the true distribution. CRPS is the integral of the squared difference between the forecast CDF and the observation's step function, strictly proper for finite first moment (secondary sources only; full text not read). Murphy 1973 splits the mean Brier score into reliability (calibration), resolution (discrimination) and uncertainty (secondary source only). [recall] Brier 1950, Monthly Weather Review 78:1-3. BSS = 1 - BS/BS_ref, where BS_ref = base-rate climatology, = p(1-p) for a constant forecast of the base rate p. POD, FAR, CSI and lead time come from the NOAA/WMO warning-verification literature (e.g. Brooks & Correia on tornado warnings). I found no URL for these, so: not found.

2. Human calibration. Mellers et al. 2014 (Psych Sci 25(5):1106-1115, doi 10.1177/0956797614524255): I did not read the paper. The training figures I found are from related papers. Chang, Chen, Mellers & Tetlock 2016 (JDM 11(5)) report that sub-hour "CHAMPS KNOW" training improved Brier scores 6-11% over control. Tetlock, Mellers, Rohrbaugh & Chen 2014 (Curr Dir Psych Sci) credit debiasing training and teaming with roughly 10% each. The aggregation gain (extremized weighted averages beating the best individuals) is [recall] and unverified. Tetlock 2005 (Expert Political Judgment, Princeton UP) is [recall]: experts were overconfident and barely beat simple extrapolation baselines. Superforecasting (2015) is [recall] too.

3. Temporal validation. Croushore & Stark 2001, "A Real-Time Data Set for Macroeconomists," J. Econometrics 105:111-130, is the recommended citation on the Philadelphia Fed page (read). The page defines vintages as snapshots of each series as reported at a given date, with the same period taking different values across vintages. The page does not argue why revised data is wrong. The reason is that revised data leaks information unavailable at forecast time, so scoring pre-revision forecasts against it is invalid. Hegre et al. 2019, "ViEWS: A political Violence Early-Warning System," JPR 56(2):155-174, doi 10.1177/0022343319823860, produces 36-month monthly forecasts at country and subnational level. Its 2020 follow-up (Hegre et al., JPR, "ViEWS2020") retrospectively evaluates forecasts published from July 2018 to Dec 2019 against earlier out-of-sample 2015-17 forecasts (search snippet only). The specific competition rules and split dates: not found.

4. Platforms. Metaculus: API launched Feb 2023. A third-party blog (alphascope.app, unofficial) claims token auth is now required, Terms of Use were last modified 21 Sep 2026, and commercial use and AI/ML evaluation need written permission. The official API and terms pages returned empty content, so API terms, data licence and political-question policy are not found. That blog is the only source on licence terms and is not authoritative. Polymarket (docs.polymarket.com, read): the Gamma endpoint gamma-api.polymarket.com/markets/keyset is shown with an unauthenticated curl example. CLOB/Data APIs and geo restrictions: not found. Kalshi (docs.kalshi.com, read): offers REST, WebSocket and FIX APIs for event contracts. Whether market data needs a key, and its political categories: not found. Good Judgment Open API or export: not searched, not found. Arrow et al. 2008, Science 320:877 "The Promise of Prediction Markets" [recall, unread]. Thin-market and manipulation caveats: not sourced this session.

5. Published EW evaluations. USHMM Early Warning Project accuracy page (via search summary; direct fetch failed twice): average risk in onset years is about 3x the average in non-onset years. About 64% of onsets since 1994 appeared in the Top-30 list in the two years before. About 20 false positives per onset at a 4% threshold. A forecast of "no onset ever" would score about 99% accuracy. The page says the model is imprecise despite performing well on 3 of its 4 metrics. Only onsets count, and a forecast a year early counts as a miss. Mueller & Rauh, APSR 112(2):358-375 (2018): newspaper-topic models forecast onset 1-2 years ahead out of sample, and add the most in previously peaceful countries. Numeric results: not found. Replication data: doi 10.7910/DVN/SJ8ER9.

## Evidence

- https://journals.plos.org/plosone/article?id=10.1371/journal.pone.0118432 (read)
- https://www.philadelphiafed.org/surveys-and-data/real-time-data-research/real-time-data-set-for-macroeconomists (read)
- https://docs.polymarket.com/ and https://docs.kalshi.com/ (read, overview only)
- https://earlywarningproject.ushmm.org/accuracy (search summary only)
- https://www.prio.org/publications/11231 (ViEWS, snippet)
- https://www.metaculus.com/news/2023/02/15/metaculus-officially-launches-api/ (snippet)

## Caveats (verbatim)

Several fetches failed (EWP accuracy page directly, Metaculus API and terms pages, Kalshi sub-pages). Gneiting, Murphy, Mellers, Hegre and Mueller-Rauh rest on search snippets and secondary papers, not the primary texts. Metaculus licence terms are unverified, and a commercial or AI-evaluation use needs the official terms checked before relying on Metaculus as a comparator. Items marked [recall] must be verified before use.

## Orchestrator note

The EWP's own accuracy summary (about 64% of onsets in the top 30 two years ahead; about 20 false positives per onset at a 4% threshold; "no onset ever" scores 99%) is the model for how Canary reports its own performance: precision-recall and false-alarm ratio against base rate, never accuracy. The vintage principle from economics (score a forecast only against the data that existed when it was made) is adopted as a hard rule for backtesting in `docs/09`.
