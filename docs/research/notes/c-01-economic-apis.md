# C-01: World Bank, IMF, OECD, ILO and Our World in Data access

- Date: 2026-10-20
- Agent: researcher (Sonnet, low effort), 27 tool uses

## Answer (verbatim; read 2026-10-20; "not found" = not established from a primary page)

1. World Bank. Indicators API base is https://api.worldbank.org/v2/, with no key or authentication ("API keys and other authentication methods are no longer necessary"). The page names JSON as an option but lists no other formats, and no rate limits are documented. WDI is updated quarterly; the latest release note I found is July 2026 (national accounts and population for 2025, poverty through 2024). The default licence for World Bank-produced datasets is CC BY 4.0. Exceptions: ODbL, the Microdata Research License, "License Specified Externally" (third-party hosted), and custom licences. Check each dataset's catalog entry. WGI is annual: the 2026 edition (1996-2025) is published, and the 2025 edition had a methodology revision that recalculated history to 1996. The WGI page states no licence or API. It gives a Usage Advisory ("strictly for research, policy analysis, and government reflection") and offers Excel/Stata downloads. Global Economic Monitor and Pink Sheet cadence: not found.

2. IMF. The new portal at data.imf.org offers SDMX 2.1 and SDMX 3.0 APIs. The IMF's own Resource-Pages page says nothing about authentication for data requests or about rate limits (not found). Swagger exploration at portal.api.imf.org needs an account. The legacy portal was retired on 5 Nov 2025 (IMF notice extauth.imf.org). Secondary sources say dataservices.imf.org was decommissioned; I could not probe it live because the sandbox blocked the host. IFS is no longer a single dataset and is split across other datasets. A confirmed list of reachable datasets (WEO, BOP, FSI) was not obtained. Terms (imf.org Copyright-and-Terms): users may "download, copy, adapt, publish, and distribute" IMF data with attribution ("Source: International Monetary Fund, Database Name, <<link>>") and must state material transformations. Fair use is authorised "for noncommercial purposes". For commercial reuse, "email copyright@imf.org to request permission". The IMF is therefore not CC BY.

3. OECD. The endpoint is https://sdmx.oecd.org/public/rest/ (SDMX-REST) and needs no authentication. Rate limits: the English explainer says a maximum of 60 data downloads per hour, with VPN/anonymised traffic disallowed. A second OECD page version says 20 queries per minute and 20 downloads per hour. Some parameters are restricted and return 413. I could not open the live page myself (403), so I only have the search-engine excerpt. CC BY 4.0 for OECD data: not confirmed. A third-party directory says the APIs are offered subject to the OECD Terms and Conditions, and the terms page returned 403.

4. ILO. ILOSTAT has an SDMX API (sdmx.ilo.org) and a bulk download facility (ilostat.ilo.org/data/bulk/; files are csv.gz plus dictionary csv; guidelines updated 16 Feb 2024). Per a secondary source (Rilostat help), the SDMX API caps at 300,000 records per request, and the R package Rilostat is a wrapper. Licence (CC BY 4.0?): not found. Update cadence: not found. ILO pages returned 403.

5. OWID. Chart data is at https://ourworldindata.org/grapher/{slug}.csv, with parameters csvType=full|filtered, useColumnShortNames, v and nocache. Metadata is at {slug}.metadata.json (accepts only slug and nocache) and returns chart settings, per-column details and dateDownloaded. A 403 means the data is non-redistributable. The ETL catalog (Tables API) serves Parquet/Feather at https://catalog.ourworldindata.org/[channel]/[dataset]/[version]/[dataset]/[table].parquet, or via `pip install owid-catalog` and fetch(). OWID documents no rate limits and says the APIs are under active development. Licence: OWID-produced data is CC BY 4.0. Third-party data keeps the provider's licence. Origins are shown through source labels ("processed by Our World in Data") and citations on "Learn more about this data". The exact licence field name in the metadata JSON was not verified.

## Evidence

- https://datacatalog.worldbank.org/public-licenses — CC BY 4.0 default plus exceptions
- https://datahelpdesk.worldbank.org/knowledgebase/articles/889392-about-the-indicators-api-documentation — v2, no key
- https://datatopics.worldbank.org/world-development-indicators/release-note/jul-2026.html — quarterly WDI update (search excerpt only)
- https://www.worldbank.org/en/publication/worldwide-governance-indicators — WGI 2026 release, Usage Advisory
- https://data.imf.org/en/Resource-Pages/IMF-API — SDMX 2.1 and 3.0
- https://extauth.imf.org/maintenance/LegacyDataPortalRetired.html — legacy portal retired (search excerpt only)
- https://www.imf.org/en/About/Copyright-and-Terms — reuse terms
- https://www.oecd.org/en/data/insights/data-explainers/2024/11/Api-best-practices-and-recommendations.html — rate limit (search excerpt only)
- https://ilostat.ilo.org/data/bulk/ and https://webapps.ilo.org/ilostat-files/Documents/ILOSTAT_BulkDownload_Guidelines.pdf — bulk facility (search excerpt only)
- https://docs.owid.io/projects/etl/api/chart-api/ — CSV and metadata.json formats
- https://docs.owid.io/projects/etl/api/catalog-api/ — catalog URL pattern
- https://ourworldindata.org/faqs — licensing

## Caveats (verbatim)

The sandbox blocked direct API probes, and oecd.org, ilostat.ilo.org and ourworldindata.org returned 403 to the page fetcher. The OECD and ILO items therefore rest on search excerpts or are marked not found. The two OECD rate-limit versions disagree (60/hour against 20/minute and 20/hour). The IMF legacy retirement date comes from search excerpts, and a May 2025 library article gave a different, earlier date (30 June 2025). No live API call was made to any source.

## Orchestrator note

The IMF's 2025 portal migration retired an API many projects depended on; it is a second concrete case for the source-registry rule that every adapter records the access regime it was built against and is health-checked. For the first phase, World Bank (CC BY 4.0, no key) and OWID (CC BY 4.0 for OWID-produced series, upstream licence preserved in metadata) carry the economic layer; IMF SDMX follows once its auth and limits are confirmed by a live call.
