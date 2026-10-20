# A-05: Transparency International CPI, OpenSanctions, GeoNames, Wikidata, Natural Earth

- Date: 2026-10-20
- Agent: researcher (Sonnet, low effort), 12 tool uses

## Answer (verbatim; all pages read 2026-10-20)

1. TI CPI: Latest is CPI 2025, released 10 Feb 2026 (annual, historically Jan/Feb; year selector lists 1995-2025). Download is XLSX only (no CSV listed): https://images.transparencycdn.org/images/CPI2025_Results.xlsx; methodology ZIP at https://images.transparencycdn.org/images/CPI-2025-Methodology.zip. Licence: "Except where otherwise noted, this work is licensed under CC BY-ND 4.0" (so redistribution unchanged with credit; no derivatives). TI terms: "Our status as the authors of content on our websites must always be acknowledged." Caveats TI states: "only CPI results from 2012 onwards can be compared"; scores reflect perceptions of experts and businesspeople, not measured corruption; small year-on-year changes are usually not significant; recent cases may take a year or more to show; money laundering and foreign bribery are not measured.

2. OpenSanctions: Contains sanctions, regulatory and PEP data (Default dataset), a separate PEP dataset, and collections for Consolidated Sanctions, Securities, Maritime and KYB. The API lists 470+ sources and over 2.0M entities. "Entities of interest" is not named on pages read. Bulk formats are FollowTheMoney JSON, CSV, plain text and Senzing; daily delta files exist. The hosted API is yente-compatible, and yente can be self-hosted (/docs/on-premise/). Licence: CC BY-NC 4.0 on the licensing page footer; bulk page: "commercial use of the data requires a data license" (screening licence for internal use, reseller/OEM licence; quote from sales). Hosted API credits, excl. VAT: 500 for EUR 50; 5,000 for EUR 400; 30,000 for EUR 2,000; 100,000 for EUR 5,000; 500,000 for EUR 15,000; 1M+ by contact. Credits last one year; new business sign-ups get 2,000 free. Data updates 4 times a day.

3. GeoNames: Place names, coordinates and admin hierarchy (page text did not enumerate these, so from general knowledge, unverified here). Bulk: daily allCountries.zip plus per-country files and a separate postal-code download from download.geonames.org/export/dump/. Licence: CC BY ("credit GeoNames with a link"); "commercial usage is allowed"; data is as is. Free web services: 10,000 credits/day and 1,000/hour per username. Heavy use: the page gives no explicit self-host recommendation; it points professionals to the Premium Data Subscription and premium services with SLA. Using the daily dump is the obvious alternative but is not stated as a recommendation.

Wikidata: structured data in main, Property, Lexeme and EntitySchema namespaces is CC0 ("released into the public domain under Creative Commons Zero"); other namespaces are CC BY-SA 4.0. Natural Earth: "All versions of Natural Earth raster + vector map data ... are in the public domain."

## Evidence

- https://www.transparency.org/en/cpi/2025 — XLSX links, CC BY-ND 4.0, 182 countries
- https://www.transparency.org/en/terms — attribution clause; CC BY-ND
- https://www.transparency.org/en/news/how-cpi-scores-are-calculated — 2012 comparability, perception caveats
- https://www.opensanctions.org/licensing/ — CC BY-NC 4.0, commercial licences
- https://www.opensanctions.org/docs/bulk/ — formats, commercial-use clause
- https://www.opensanctions.org/api/ — pricing, 4x daily updates, datasets
- https://www.opensanctions.org/docs/faq/ — yente on-premise pointer
- https://www.geonames.org/export/ — licence, downloads, limits
- https://www.wikidata.org/wiki/Wikidata:Licensing — CC0
- https://www.naturalearthdata.com/about/terms-of-use/ — public domain

## Caveats (verbatim)

/pricing/ on OpenSanctions returned 404. Prices come from /api/ and may change. The CPI XLSX year range was not confirmed from the file itself. The TI terms page governs the website. The CPI data licence is CC BY-ND, not CC BY. The TI terms also say the site is for "domestic and private use"; that clause is in tension with CC BY-ND reuse, so check with TI before commercial redistribution. I did not open yente docs or the GeoNames readme/credits pages.
