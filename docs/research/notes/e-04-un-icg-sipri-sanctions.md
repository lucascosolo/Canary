# E-04: UN feeds and terms, CrisisWatch and CFR tracker, SIPRI, sanctions lists, GPI and FSI

- Date: 2026-10-20
- Agent: researcher (Sonnet, low effort), 24 tool uses

## Answer (verbatim; fetched 2026-10-20; much is only partly established)

1. UN. press.un.org: RSS page /en/rss returned 404; feed URL not found. news.un.org/en/rss-feeds: HTTP 403, not found (UN News is widely known to offer per-topic RSS, unverified here). Digital Library (digitallibrary.un.org) OAI-PMH/search API: 403, not found. Security Council Report Monthly Forecast (securitycouncilreport.org/monthly-forecast): published monthly, footer RSS icon links to /index.xml (unconfirmed; the page did not say so explicitly); copyright (c) 2026 Security Council Report, Legal/Permissions pages not read, licence not found. UN terms of use (un.org/en/about-us/terms-of-use): download/copy for personal, non-commercial use only, no resale, redistribution or derivative works; attribution not addressed. un.org/en/about-us/copyright: "all rights reserved"; news-related material usable with credit and notification to the UN; other permissions via shop.un.org/rights-permissions. So UN content is NOT generically free to reuse with attribution; carve-outs may exist per document or dataset.

2. CrisisWatch (crisisgroup.org/crisiswatch): 403, so monthly structure, flags, RSS/API and terms are not found. Terms page (crisisgroup.org/terms-use) also 403. CFR Global Conflict Tracker (cfr.org/global-conflict-tracker): interactive tracker from CFR's Wachenheim Center for Peace and Security, 27 conflicts in 5 regions, filters by type, status (worsening/improving/unchanging/developing) and US impact; no download/CSV/API stated; page embeds JSON-LD listing the 27 conflicts (names and URLs only); reuse terms not found.

3. SIPRI (sipri.org/databases): Arms Industry, Arms Transfers, Military Expenditure, Multilateral Peace Operations databases, plus embargoes, National Budget Archive and others. Arms Transfers (sipri.org/databases/armstransfers): updated 9 March 2026, covers 1950-2025, annual cadence; export formats not stated on the page (query tool at armstransfers.sipri.org; xlsx not confirmed). Terms (sipri.org/databases/terms): citation without permission in papers, articles, blogs if SIPRI is named; reproduction needs authorisation unless fair use (non-commercial AND under 10% of a dataset); commercial use (including ratings, statistical products, internal business tools) needs a licence, case by case. So: free with citation for analysis, restricted for redistribution and commercial use.

4. Sanctions. OFAC Sanctions List Service (ofac.treasury.gov/sanctions-list-service; sanctionslist.ofac.treas.gov/Home/SdnList, /ConsolidatedList, /CustomizeSanctionsDataset, /DeltaFileArchive): Advanced Sanctions Data Model (XML) and legacy flat files, delta files; no auth stated; cadence not stated (updated on action, per Recent Actions). EU consolidated list: per OpenSanctions, source is XML at webgate.ec.europa.eu/fsd/fsf/public/files/xmlFullSanctionsList_1_1/content?token=dG9rZW4tMjAxNw ; cadence of the source not stated, data.europa.eu page gave no values. UN SC consolidated list (main.un.org/securitycouncil/content/un-sc-consolidated-list): page returned empty; XML URL and cadence not found. OpenSanctions (opensanctions.org/datasets/) lists a "Consolidated Sanctions" collection of lists from different countries and bodies (104,665 entities) and ingests the EU list, but the page did not name OFAC or UN explicitly; licence CC BY-NC 4.0, with paid commercial licences; bulk JSON/CSV/Senzing exports; EU dataset processed 2026-10-20.

5. Indices. GPI (visionofhumanity.org/maps, /resources): 2026 edition, 163 countries; free PDFs (report, briefing, wall chart); no raw dataset or licence on the pages read; /terms/ not read. Fragile States Index (fragilestatesindex.org/excel/): xlsx per year 2006-2023 listed under /wp-content/uploads/ (e.g. FSI-2023-DOWNLOAD.xlsx); no licence stated; later years not listed. Critique: "Handle with care!", Development and Change, 2018, DOI 10.1111/dech.12417 (aggregation, conflation of causes and consequences), found via search summary only.

## Evidence

- https://www.un.org/en/about-us/terms-of-use and /copyright — as above
- https://www.sipri.org/databases/terms and /databases/armstransfers — as above
- https://www.opensanctions.org/datasets/eu_fsf/ — EU source URL and format
- https://ofac.treasury.gov/sanctions-list-service — formats and URLs
- https://www.cfr.org/global-conflict-tracker; https://fragilestatesindex.org/excel/; https://www.securitycouncilreport.org/monthly-forecast

## Caveats (verbatim)

403/404 on press.un.org RSS, news.un.org, UN Digital Library, crisisgroup.org (both pages); UN SC list and data.europa.eu returned empty. The fetcher summarises pages with a small model, so treat details as unverified. The FSI critique DOI was not opened. Items marked "not found" need a browser or direct curl.

## Orchestrator note

CrisisWatch and the UN sites block the fetcher, which says nothing about their terms; both need a browser read in a later session. SIPRI's fair-use carve-out (non-commercial and under 10% of a dataset) fits a dashboard that shows a country's arms-import trend but not one that mirrors the database. Sanctions designations are best taken from OpenSanctions (CC BY-NC, daily deltas) rather than from the three raw lists.
