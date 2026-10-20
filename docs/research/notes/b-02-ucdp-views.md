# B-02: UCDP datasets and API, ViEWS forecasts, UCDP-ACLED comparisons

- Date: 2026-10-20
- Agent: researcher (Sonnet, low effort), 8 tool uses

## Answer (verbatim)

1. UCDP (read 2026-10-20). The API at https://ucdp.uu.se/apidocs/ requires a token, confirmed. Send it in the HTTP header `x-ucdp-access-token`. To request one, email the API maintainer, Mert Can Yilmaz (mertcan.yilmaz@pcr.uu.se), with your name, affiliation, role and intended use. The page says requests are answered "within 3-5 working days". The API is free, the quota is 5,000 requests a day (errors count), and every request must specify a version number.
- Bulk downloads from https://ucdp.uu.se/downloads/ are direct links to zip/CSV/Excel files. The page shows no token requirement for them.
- Terms for all datasets: "free of charge and licensed under CC BY 4.0", and the listed publications must be cited.
- GED: v26.1, 1989-2025. Coverage years are inferred from the citation title. CSV is https://ucdp.uu.se/downloads/ged/ged261-csv.zip, with an Excel version alongside. Update cadence is not stated. The API page lists 26.1 as the latest.
- UCDP Candidate: v26.0.8 (August 2026), monthly releases lagging by no more than a month, global, CSV/Excel (https://ucdp.uu.se/downloads/candidateged/GEDEvent_v26_0_8.csv). The API also lists a quarterly release, 26.01.26.06.
- UCDP/PRIO Armed Conflict: v26.1, 1946-2025, conflict-year data where at least one party is a state government. CSV is https://ucdp.uu.se/downloads/ucdpprio/ucdp-prio-acd-261-csv.zip. Cadence is not stated.
- The 25-deaths threshold was not on the pages I read, so I'm giving it from background knowledge: an armed conflict needs at least 25 battle-related deaths in a calendar year. Verify it in the codebooks.

2. ViEWS. The site (https://viewsforecasting.org/) says it publishes open-access monthly forecasts of state-based armed conflict, country and sub-national, 1-36 months ahead. The latest release covers Sep 2026 to Aug 2029. Geo-referenced forecasts are at 0.5 degree (PRIO-GRID) resolution for Africa and the Middle East. The header says "New forecasts released every month", but the news items I saw were dated 30 Jun and 30 Sep 2026, which looks quarterly. Forecasts can be explored at data.viewsforecasting.org and downloaded from a Data Access page. The site does not mention an API, but the GitHub org lists a `views_api` repo ("Documentation of the VIEWS API") and a `viewser` CLI. No license was stated on the site or the GitHub org page. Code is on GitHub under the organisation prio-data, with repos viewsforecasting, views_pipeline, viewser, views_api, views_outreach and prediction_competition_2023.
- Evaluation: Vesco, Hegre, Colaresi, Jansen, Lo, Reisch and Weidmann (2022), "United they stand: Findings from an escalation prediction competition", International Interactions 48(4): 860-896. Its finding: a simple ensemble of the competition entries beat the average individual model. Companion paper: Hegre, Vesco and Colaresi, "Lessons from an Escalation Prediction Competition", also in International Interactions 48 (2022). Hegre et al. 2019, JPR 56(2), "ViEWS: A political violence early-warning system", is cited from memory only and I did not verify it. I found no 2024 evaluation paper.

3. UCDP vs ACLED.
- Eck (2012), "In Data We Trust? A Comparison of UCDP GED and ACLED Conflict Events Datasets", Cooperation and Conflict 47(1): it finds both datasets rely on media reporting, and it advises caution with ACLED for sub-national work because of uneven quality control. ACLED includes non-violent events that UCDP does not code. Only the abstract-level summary was read.
- Öberg and Yilmaz (2025), Research & Politics: a critique responding to a Raleigh, Kishi and Linke comparison of UCDP and ACLED. I only saw its title and listing, so I cannot state its finding.

## Evidence

- https://ucdp.uu.se/apidocs/ — token header, how to request, 5,000 requests a day, versions
- https://ucdp.uu.se/downloads/ — dataset versions, coverage years, URLs, CC BY 4.0
- https://viewsforecasting.org/ — forecast scope, release dates, downloads
- https://github.com/prio-data — ViEWS repos
- https://www.prio.org/publications/13337 — competition paper (via search)
- https://library.alnap.org/node/64946 — Eck 2012 record
- https://doaj.org/article/a9fe5df517e34e3288fefc54086af44f — Öberg and Yilmaz 2025 listing

## Caveats (verbatim)

WebFetch output is summarised by a small model, so the CC BY 4.0 quote and the details above are not verbatim page text. The /data-access/ page on viewsforecasting.org returned 404, so ViEWS download formats, license and the actual ViEWS API status are unverified. Several repo licenses were not checked. The Hegre 2019/2021/2024 JPR papers were not read.

## Orchestrator note

UCDP is the cleanest conflict-event source available: CC BY 4.0, bulk CSV without a token, monthly Candidate releases, and a free token-gated API with a 5,000/day quota. It becomes the primary conflict-event source; its 25-death threshold and media dependence are documented limitations to show in the UI.
