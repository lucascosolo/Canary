# H-02: Displacement data sources and regional public-opinion programmes (verification of user list, second half)

- Date: 2026-10-20
- Agent: researcher (Sonnet, low effort), 35 tool uses

## Answer (verbatim; date read 2026-10-20)

Verification from organisations' own pages was only partly possible (several sites returned 403/404 or JS-only shells to the fetcher).

1. UNHCR Refugee Data Finder API: REST, base https://api.unhcr.org/population/v1/. Endpoints: /population/, /asylum-applications/, /asylum-decisions/, /solutions/, /demographics/, /unrwa/, /idmc/ (IDPs due to conflict/violence), /nowcasting/ (current-year estimate), /footnotes/, /countries/, /regions/, /years/. Plain GET, Accept: application/json, no credentials shown in examples (no auth documented). Licence: NOT FOUND (CC BY 4.0 not confirmed; unhcr.org terms pages returned 403). Cadence: mid-year release (Mid-Year Trends 2025 exists, with preliminary figures) plus annual Global Trends; the docs page states no refresh schedule.

2. IOM DTM: API on the DTM Developer Portal; registration and a subscription key are required. v3 live Aug 2025; v1/v2 unmaintained. IDP API (country/admin1/admin2, "non-sensitive IDP figures") and HNA API (admin2, IDPs/returnees/non-displaced, min. 10 households). Clients: Python dtmapi, R. Terms (dtm.iom.int/terms-and-conditions) are restrictive: materials "may be viewed, downloaded, and printed for non-commercial use only"; no resale, redistribution or derivatives; extraction/reproduction/distribution "requires the explicit prior written permission of IOM"; mandatory credit line "Source: International Organization for Migration (IOM), [month, year], Displacement Tracking Matrix (DTM)". Not an open licence. Cadence: not found.

3. IDMC: NOT ESTABLISHED. The GIDD, API and terms pages returned only navigation or footers. Known only: API host api.internal-displacement.org appears in site assets, and the OCHA-DAP R package "idmc" says the IDU endpoint URL is supplied by IDMC (the key/URL process is unconfirmed). Licence, GIDD download terms and cadence: not found. UNHCR's /idmc/ endpoint republishes IDMC conflict IDP stock.

4. WFP HungerMap LIVE: API, auth, licence, cadence all not found (hungermap.wfp.org is JS-rendered; docs.wfp.org returned 403). WFP press describes the platform as covering 50+ countries, with near-real-time monitoring planned for up to 60.

5. FEWS NET: fews.net/data redirects (301) to https://fdw.fews.net/data-explorer/ (the Famine Early Warning Systems Network Data Warehouse), but that returned 403. API, licence (public domain?) and outlook cadence: not found.

6. Surveys (can aggregates go on a public non-commercial dashboard with attribution?):
- WVS: terms page is empty in the fetch; wave 7 (2017-2022) data downloadable; wave 8 appears in the nav with no details. Registration, non-redistribution terms and wave 8 timing: not found. Dashboard use of aggregates: unconfirmed, so ask jdiezmed@jdsurvey.net.
- ESS: data portal ess.sikt.no, rounds ESS1-11 plus CRONOS; ESS11 edition 4.2 published 2 July 2026. Citation is required. Licence (CC BY-NC-SA?) and registration: not confirmed.
- Afrobarometer: "data are protected by copyright"; no named licence. Public datasets need no stated registration. Early access and restricted geocoded data go through a request form. Citation format is mandatory. No API; online analysis tool only. Redistribution is not addressed.
- Arab Barometer: free download after a short form (name, email, country, institution, purpose). Waves I-VII data are listed; Wave IX (Sept 2025-May 2026) has no dataset listed, and Wave VIII's link is a placeholder. Terms sit in a separate "Reprints, Permissions & Use Policy" page, not read.
- Latinobarómetro: the site offers documentation, aggregate data by wave and an online analysis tool. Registration and terms: not found.
- Asian Barometer: application-based access (data-release page and application-count statistics). Terms: not found.
- ISSP: via GESIS. Modules listed through 2024; Work Orientations V (2025) first partial release expected spring 2027. Registration and terms: not found.

## Evidence

- https://api.unhcr.org/docs/refugee-statistics.html — endpoint list, GET with no credentials (read 0-200k chars of 351k)
- https://dtm.iom.int/data-and-analysis/dtm-api — key via developer portal, v3, coverage, citation
- https://dtm.iom.int/terms-and-conditions — non-commercial only, permission required
- https://www.europeansocialsurvey.org/data-portal — ESS11 4.2 dated 2 July 2026
- http://www.afrobarometer.org/data/data-usage-and-access-policy/ — copyright, citation, no API
- https://www.arabbarometer.org/survey-data/data-downloads/ — registration form
- https://www.issp.org/data-download/by-year/ — module schedule
- https://www.worldvaluessurvey.org/WVSDocumentationWV7.jsp — wave 7 only

## Caveats (verbatim)

Most licence, auth and cadence items are "not found". UNHCR terms, WFP docs, FEWS NET FDW, ESS conditions and GESIS returned 403/404. The IDMC and WVS terms pages rendered empty. No claim of CC BY 4.0 or public-domain status is verified for any source. The fetcher summarises pages with a small model, so quotes are secondhand. Next step: read the pages in a real browser, or email the data teams. DTM's terms mean a public dashboard needs IOM written permission.

## Orchestrator note

UNHCR's API (no auth, broad endpoints) is the displacement source for the first release once its licence is read in a browser; IOM DTM is out without written permission; the survey programmes enter the catalog as "published aggregates with attribution, after confirming terms", never as microdata.
