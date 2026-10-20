# E-02: Election calendars and results, party position datasets, observation reports

- Date: 2026-10-20
- Agent: researcher (Sonnet, low effort), 25 tool uses

## Answer (verbatim; checked 2026-10-20)

Open, bulk-downloadable sources: IPU Parline (open data plus an API), PopuList v4.0 (CSV), ParlGov (Harvard Dataverse, but retiring), V-Party v2 (Feb 2022), NELDA v6. Restricted: Manifesto Project (research-only, no redistribution, API key needs an account) and ElectionGuide (free non-commercial use, no public API found). Observation reports are PDFs and web pages, with no feed or API found. For the aim, the best combination is ElectionGuide (calendar) with Parline (results and composition), then Manifesto (what parties propose) and V-Party (illiberalism and anti-pluralism scores).

1. ELECTIONS
- ElectionGuide, https://www.electionguide.org/. Provides election calendar, results and candidate data worldwide. Access is through "Access Options" (/p/access/) and "Request Credentials" (/request_access/), which I did not read. No public API or export link is visible. Terms (/p/use/): free for personal and non-commercial use (research, teaching) with attribution. Changes must be flagged. Commercial use needs a licence. Surveillance, targeted political influence and predictive markets are banned. No licence name is given. Cadence: not found.
- IPU Parline, https://data.ipu.org/. Covers about 188 parliaments and 600 fields on structure, composition and elections. Search snippets describe it as open data with a "Parline API", a data explorer and a data catalogue (data.ipu.org/data-catalogue). The licence, endpoints and auth were not found. Direct fetches returned 403, so I relied on search snippets. Cadence: not found.
- NELDA, https://nelda.co/. Covers 1945–2020 for all independent states, including microstates in v6. Latest is Version 6, with a PDF codebook, a data download form and a Stata .do file. Dataset format is not stated. No licence is stated, and the page asks users to cite Hyde & Marinov 2012. It codes election conduct, not results.
- Wikidata: not fetched. From general knowledge, it is CC0 and community-edited, so election dates and results are patchy and uneven by country. Use it for cross-checking only.

2. PARTY POSITIONS
- Manifesto Project, https://manifesto-project.wzb.eu/. Codes party manifestos. API root is https://manifesto-project.wzb.eu/api/v1/, returns JSON, and has daily quotas. An account and API key are needed (a few metadata calls need none). The R package is manifestoR. The Terms of Use (/information/documents/terms_of_use) say: scientific research only, no redistribution without written permission, and cite the work. Latest version and country count were not stated on the pages read. The API examples use MPDS2023a, and South America has been merged in since 2023a.
- V-Party, https://v-dem.net/data/v-party-dataset/. Version 2, February 2022. The Country-Party-Date file comes in SPSS, Stata, CSV and R. The Coder-Level file is CSV only. The v2 codebook (https://www.v-dem.net/documents/6/vparty_codebook_v2.pdf) lists the Anti-Pluralism Index as v2xpa_antiplural, scaled 0 to 1. It is built from four indicators: commitment to the democratic process, demonization of opponents, political violence, and minority rights. Coverage is stated inconsistently (see caveats). Licence not found. The codebook says "All rights reserved". I did not confirm a CC BY-SA licence, and I did not confirm the illiberalism index.
- PopuList, https://popu-list.org/. Classifies European parties as populist, far-right, far-left or Eurosceptic. Covers 31 countries, 1989 to 2026. Version 4.0, launched May 2026. Downloads are a dashboard, a PDF, a CSV, Excel files for v1–v4, and OSF/GitHub. The site shows only a copyright notice, and no licence was found.
- ParlGov, https://parlgov.org/. Covers EU and OECD democracies, 1900–2023. Data is on Harvard Dataverse, with a GitHub R snippets page. The latest release noted is "ParlGov 2024 released" (2024-08-12). A 2024-10-01 post, "Retiring from ParlGov", suggests no further updates. Format and licence not found.

3. OBSERVATION
- OSCE/ODIHR, https://www.osce.org/odihr/elections. The fetch failed on a certificate error, so archive, RSS and API are all not found.
- Carter Center, https://www.cartercenter.org/news/publications/election_reports.html. A filterable archive of reports and statements. The newest listing is a Palestinian municipal elections final report (2026-07-20). Licence, RSS and API: not found.
- EU EOM, https://www.eeas.europa.eu/. The page I tried returned 404, so reports, feeds and reuse terms are not found.
- OAS, https://www.oas.org/eomdatabase/. A searchable database of missions and recommendations, 1962–2026, 34 member states. Downloads and licence were not confirmed.
- PEI (Electoral Integrity Project), https://electoralintegrityproject.com/. The site points to Harvard Dataverse. Latest version, coverage and licence were not retrievable.

## Evidence

- https://www.electionguide.org/p/use/ — use policy
- https://nelda.co/ — NELDA v6, 1945–2020
- https://manifesto-project.wzb.eu/information/documents/api — API and key
- https://manifesto-project.wzb.eu/information/documents/terms_of_use — research-only terms
- https://v-dem.net/vpartyds.html — V-Party v2, formats
- https://www.v-dem.net/documents/6/vparty_codebook_v2.pdf — codebook (seen via search snippet only)
- https://popu-list.org/ — v4.0
- https://parlgov.org/ — 1900–2023, retiring
- https://data.ipu.org/about — Parline (search snippet only)
- https://www.oas.org/eomdatabase/ — OAS database

## Caveats (verbatim)

The IPU, ODIHR, EU and PEI pages failed or were empty, so those entries are incomplete. V-Party coverage figures conflict: 169 countries (Wikipedia), 1970–2019 (CRC 1342), and since 1990 (other). No licence was found for any dataset except the ElectionGuide and Manifesto terms. The V-Party "illiberalism" index was not confirmed. The Wikidata line and the V-Party codebook detail rest on search snippets or general knowledge.

## Orchestrator note

The election layer for a first release is: ElectionGuide for the calendar (non-commercial terms satisfied; credentials to request), IPU Parline for results and composition (open data, API to confirm), V-Party's anti-pluralism index (v2xpa_antiplural) as the quantitative anchor for "parties proposing to restrict liberties" (coverage ends 2019 in v2; a newer version is to be checked), and observation-mission reports as linked documents with claims extracted from their executive summaries. The Manifesto Project is research-only with no redistribution, so it is out for a public dashboard.
