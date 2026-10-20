# E-03: Human-rights documentation and index sources

- Date: 2026-10-20
- Agent: researcher (Sonnet, low effort), 23 tool uses

## Answer (verbatim; fetched 2026-10-20)

1. UN. spcommreports.ohchr.org (Special Procedures communications since 2011): its own page mentions search/export options, an API and RSS feeds (details/endpoints not found). UN Digital Library (digitallibrary.un.org, Invenio): OAI-PMH endpoint https://digitallibrary.un.org/oai2d (Identify verb; guide is generic Invenio, supported formats/sets unverified); also has a Record API help page. Auth: not found. ODS, UPR and treaty-body systems: not found/not read. OHCHR and UN Digital Library pages returned 403 to my fetcher. UN terms: un.org terms-of-use allow download/copy for personal, non-commercial use only, no resale, redistribution or derivative works; UN copyright page says nothing may be reproduced without written permission of UN Publications, except news material (credit and notify the UN). So "free with attribution" is NOT confirmed; a blanket UN document reuse licence was not found.
2. Indices.
- PTS (politicalterrorscale.org/Data/Download.html): 1976 onward; Amnesty 1976-2025, State Dept 1976-2024, HRW 2013-2025; PTS-2026 release updated Sept 2026; .csv/.xlsx/.dta/.RData, codebook v2.40; Societal Violence Scale 2013-16 xlsx. Licence: not stated on the page. Free download, no auth seen. Annual.
- CIRIGHTS (cirights.com): all countries, "40 years" (exact range not stated); v3.12.10.24 as .dta (zip) and .xlsx; licence not stated, citation of Scoring Manual V2.11.06.23 (SSRN 4625036) requested. No API found.
- HRMI (rightstracker.org): civil/political rights via expert survey, economic/social via statistics (my background knowledge; the about page returned 429). Download page humanrightsmeasurement.org/download-the-dataset/ lists 2026 dataset plus archives 2019-2025 and 2017/18. Licence CC BY-NC 4.0 on main and download pages (commercial use: contact HRMI); an embargoed-data page says CC BY 4.0. API: not found. Annual.
- Academic Freedom Index (academic-freedom-index.net): 179 countries and territories, assessments as of Dec 2025, Update 2026 report PDF; site content CC BY 4.0; dataset is V-Dem (data v16), dataset licence not stated on this page. Underlying data format: not stated here.
3. NGOs.
- HRW: RSS exists (hrw.org/rss, live, many items). Reuse terms: hrw.org/terms-of-use returned 404; not found. No API found.
- Amnesty: RSS page and terms URLs returned 404; not found.
- Front Line Defenders (frontlinedefenders.org/en/global-analysis): Global Analysis 2025/26 dated 15 June 2026; older editions PDF, 2024/25 a Shorthand story; no data download or licence stated.
- Global Witness (globalwitness.org/en/campaigns/environmental-activists/): annual reports since 2012; latest "at least 124 killed in 2025", 16 Sept 2026; footer "© Global Witness 2026"; no data download or licence on page (archive page not read).
- Scholars at Risk: Free to Think 2026 released 15 Sept 2026 (382 attacks). From 1 July 2026 SAR no longer publishes reports on individual incidents it records; no export or licence stated.
- HURIDOCS Uwazi (uwazi.io): open-source database software to collect, manage, analyse and publish information (custom templates, PDF metadata extraction, many languages, roles); MIT licence.

## Evidence

- https://www.politicalterrorscale.org/Data/Download.html — coverage, formats, no licence
- https://cirights.com/ — formats, citation
- https://www.academic-freedom-index.net/ — 179 countries, CC BY 4.0 site
- https://www.un.org/en/about-us/terms-of-use ; https://www.un.org/en/about-us/copyright — restrictive terms
- https://spcommreports.ohchr.org/ — mentions export, API, RSS
- https://digitallibrary.un.org/oai2d — endpoint named in search-result snippets of the UN help guide (https://digitallibrary.un.org/help/oairepository-admin-guide)
- https://uwazi.io/ — MIT
- https://www.hrw.org/rss ; https://www.globalwitness.org/en/campaigns/environmental-activists/ ; https://www.frontlinedefenders.org/en/global-analysis ; https://www.scholarsatrisk.org/actions/academic-freedom-monitoring-project/
- HRMI licence from a web search summary of humanrightsmeasurement.org/download-the-dataset/ (not read directly)

## Caveats (verbatim)

Many primary pages blocked (403/404/429), so OHCHR, ODS, UPR, treaty bodies, Amnesty, HRW terms, and the HRMI about page are unverified. HRMI licence conflicts (NC vs BY). UN Digital Library OAI details come from search snippets, not a live request. Fetch summaries are model-generated.

## Orchestrator note

Two patterns recur across this wave: NGO reports are reachable by RSS but their reuse terms are usually unstated, so Canary stores metadata, links and short excerpts, never full text; and the UN's general terms are more restrictive than commonly assumed, so UN documents are linked and summarised in Canary's own words, with the document ID and URL kept as provenance. The annual indices (PTS, CIRIGHTS, HRMI, AFI) are inputs to the baseline layer, not to near-term change detection.
