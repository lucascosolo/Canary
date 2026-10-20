# H-01: Verification of user-suggested sources (first half)

- Date: 2026-10-20
- Agent: researcher (Sonnet, low effort), 28 tool uses
- Context: the user pasted a fifty-item source list (note USER-02) and asked that it be taken with a grain of salt.

## Answer (verbatim; read 2026-10-20; many pages were JS-rendered, blocked (403) or had cert errors, so several items are "not found")

1. UN Peace & Security Data Hub, https://psdata.un.org/: the page loads (title "Peace & Security Data Hub") but the fetch returned only the title. Operator, datasets, API, licence, cadence: not found. Whether it exists is confirmed only by the title. The "DPPA/DPO" guess and "peacekeeping/Security Council datasets" are unverified.

2. GTD (START, UMD): www.start.umd.edu/gtd/ failed (self-signed cert chain). From search results only, so secondary:
   - START's EULA (start.umd.edu/gtd-terms) grants a revocable, non-exclusive licence for non-commercial research. It bars public posting of the data or codebook.
   - A START news item says organisations, including commercial ones, must buy a licence from CHC Global. Personal and academic users download free.
   - The about page was reported as covering 1970-2020. Latest year, current registration flow, and non-profit treatment: not established.

3. WJP Rule of Law Index: the index page and downloads page gave nothing usable (403 or labels only). Search results say the 2025 edition covers 143 countries and that questionnaires and a variable map are downloadable. Past editions had Excel files (WJPIndex2025.pdf exists under /rule-of-law-index/downloads/). Licence for the 2025 data: not found. An old third-party mirror lists CC BY-ND 4.0 for 2019, which is not authoritative.

4. Global R2P: the publications page (https://www.globalr2p.org/publications/) lists Atrocity Alert No. 498 as a recent October 2026 item, with 496 and 497 just before it, so it is roughly weekly. R2P Monitor is a filterable type; its cadence is not stated. "Populations at Risk, March 2026" appears as a featured item. RSS and terms: not found. The Centre is hosted at the Ralph Bunche Institute, CUNY.

5. ICJ: the homepage (https://www.icj-cij.org/) links to case documents, RSS feeds and copyright/terms of use. The terms text and feed URLs were not read; /terms-of-use returned 404. ICC (icc-cpi.int): 403 on every fetch. Court records access, RSS and terms: not found.

6. Correlates of War (https://correlatesofwar.org/data-sets/): the page lists COW War Data 1816-2007 v4.0 (Intra-State v5.1), MIDs v5.0, NMC v7.0, State System Membership v2024, Formal Alliances v4.1, Trade v4.0, and others. Formats are not stated on the page. The terms are quoted: "By downloading a COW dataset, you agree...": "Data are not to be used for any commercial activity"; cite each dataset; no distribution to third parties without written permission from the COW director and data host. Redistribution is therefore restricted, and this is not an open licence.

7. UNSD: the UNdata terms (https://data.un.org/Host.aspx?Content=UNdataUse) say data "may be copied freely, duplicated and further distributed provided that UNdata is cited as the reference". No named licence, and no accuracy guarantee. The SDG API Swagger page (https://unstats.un.org/sdgs/UNSDGAPIV5/swagger/index.html) is titled "UNSD SDGs API", but its contents were not rendered. SDMX endpoints and SDG API terms: not found.

8. WHO:
   - GHO OData: base URL https://ghoapi.azureedge.net/api, with /Indicator, /Dimension, /WHOSIS_000001 and $filter support. The page states no licence (https://www.who.int/data/gho/info/gho-odata-api).
   - The copyright page (https://www.who.int/about/policies/publishing/copyright) says WHO publications are CC BY-NC-SA 3.0 IGO; WHO Classifications are CC BY-ND 3.0 IGO. It links a separate Data policy, which was not read.
   - The terms-of-use page allows research or private study, not commercial use, with attribution to WHO.
   - Disease Outbreak News (https://www.who.int/emergencies/disease-outbreak-news): no RSS link or cadence visible; the page rendered with no results.

9. OpenAlex:
   - The about page (https://openalex.org/about) says "Our data is CC0" and that a small nonprofit team runs it.
   - The rate-limit page (https://help.openalex.org/how-to-use-the-api/rate-limits-and-authentication) says basic queries work with no key.
   - A free API key gives a 10x daily budget and is required for cursor paging.
   - Per-second limits: 10 with no key, 30 with a free key, 50 on an annual plan. It returns 429 on excess.
   - The page does not mention a "polite pool", which looks outdated.
   - 100 results per page; basic paging stops at 10,000 results.

10. Internet Archive: the Availability API is documented at https://archive.org/help/wayback_api.php. `archive.org/wayback/available?url=...&timestamp=...` returns one closest snapshot. It also lists the Memento API and the CDX Server API. Rate limits and terms are not on that page. Save Page Now API details, auth, limits and terms: not found (the terms page rendered only a title).

## Evidence

The URLs above, each read 2026-10-20 via WebFetch. Search results supplied the GTD and WJP details.

## Caveats (verbatim)

Sandbox network policy blocked direct curl to all hosts. WebFetch hit 403 on worldjusticeproject.org downloads and icc-cpi.int, and a cert error on start.umd.edu. Items 1, 2, 3, 5 and the SDG API are mostly unverified. A browser or fetch tool allowed through the sandbox is needed to close them. I did not check whether the GHO API host is current.

## Orchestrator note

Of the user's "start with these" list, GTD (no public posting of data) and COW (no redistribution) are excluded from the public knowledge base on their own terms; UNdata's "copy freely with citation" and OpenAlex's CC0 are clean. The Internet Archive's availability and CDX APIs matter for a different reason: every cited page should be archived at citation time so the evidence trail survives link rot.
