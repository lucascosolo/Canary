# F-06: Existing monitoring platforms, commercial risk platforms, open-source projects, UN data hubs

- Date: 2026-10-20
- Agent: researcher (Sonnet, low effort), 24 tool uses

## Answer (verbatim; read 2026-10-20; WebFetch summaries, not raw pages)

1. Democracy and rights monitors
- International IDEA Democracy Tracker: monthly event analyses for 173 countries, scored against the Global State of Democracy framework. 2026 reports are published "as they are ready", with full coverage due by end-2026 while the methodology is adapted. The page states no API, bulk download or licence (T&C page not read).
- V-Dem: Dataset v16 (March 2026), annual. CC BY-SA 4.0 (commercial use allowed). ZIPs in CSV, Stata, R and SPSS, and a coder-level CSV. No API; the `vdemdata` R package is the programmatic route. Democracy Report not on that page (not verified).
- Protect Democracy Authoritarian Threat Index: US-only. It comes from the expert Authoritarian Warning Survey (since 2017) and gives a 1-5 score (3.3-3.4 "Severe" in snippets, undated). The direct URL 404'd; I read only search snippets. Data access: not found.
- Bright Line Watch: US-only expert surveys. Wave 29 was fielded 10-27 July 2026 (568 experts, plus 2,750 public respondents); report "A Partial Democratic Rebound?" (Aug 2026). Roughly every few months (cadence not stated). A "Data" section with replication material exists; terms not read.

2. Conflict and events
- ICG CrisisWatch: page returned HTTP 403. Not read. It is a monthly Crisis Group conflict digest (from memory only).
- CFR Global Conflict Tracker (Wachenheim Center): 27 conflicts, filterable by type, trend and US impact. No cadence, API or licence stated. Page JSON-LD lists the conflicts.
- ACLED CAST (the name is "Conflict Alert System", not "Conflict Alert and Severity Tracker"): six-month forecasts compared with observed counts, monthly results. It requires a myACLED login. ACLED has an API guide, but whether CAST is in it is not stated. Terms are in a separate EULA, Content Usage Terms and Attribution Policy, none read. "All content belongs to ACLED."
- Liveuamap: 403, not read. Terms and API not found.
- Wikipedia Current events portal: daily, grouped by date and category, with source links. Licence not shown in the excerpt (Wikipedia text is normally CC BY-SA; unverified here). It can be reached through the standard MediaWiki API.

3. Commercial platforms (not read; from memory, so unverified): Dataminr, Recorded Future, Janes, FiscalNote (which absorbed Predata), Seerist, Verisk Maplecroft and GeoQuant. All are paid and enterprise-only. I found no public free tier or open API for any, though I did not check each one.

4. Open source (GitHub API, 2026-10-20)
- mediacloud/web-search: 12 stars, pushed 2026-10-17, Apache-2.0. The wider org is active (metadata-lib, rss-fetcher). Media Cloud is a UMass, Northeastern and MEAG consortium with a 1bn+ story database. The site page does not mention an API; terms not read.
- ViEWS (Uppsala and PRIO): forecasts 1-36 months ahead, released monthly (latest 30 Sep 2026). Open access via data.viewsforecasting.org. A views_api repo exists. Repos: views_pipeline 7 stars, pushed 2025-01-30, license NOASSERTION; viewsforecasting 16 stars; viewser; priogrid 41 stars, pushed 2026-09-24. The site states no licence.
- OpenSanctions/yente: 182 stars, MIT, pushed 2026-10-20. The code is MIT; the OpenSanctions data licence was not checked.
- huridocs/uwazi: 328 stars, MIT, pushed 2026-10-20.
- simonw/datasette: 11,520 stars, Apache-2.0, pushed 2026-10-13.
- bellingcat: toolkit 687 stars (pushed 2026-10-20), auto-archiver 1,133 stars (MIT, 2026-09-10), ukraine-timemap 295 stars (2026-10-13).
- gdeltPyR (linwoodc3): 259 stars, GPL-3.0, last push 2023-11-30, so stale. gdelt-doc-api (alex9smith): 232 stars, MIT, pushed 2025-04-22.
- conflictforecast: no repo found at the guessed path (404).
- Search for "early warning political violence" repos pushed since mid-2024: 0 results, so no obvious competitor. Search syntax may have been too narrow.

5. UN data
- psdata.un.org (DPPA-DPO Information Management Unit): a central entry point for UN peace and security data (peacekeeping, political missions and similar). The pages are JavaScript-rendered and fetched empty. Each dataset page offers Metadata, Preview, Visualize and Download. The datasets are mirrored on HDX (data.humdata.org/organization/unpeacesecurity, ~75 datasets) through the HDX API, which is the practical API route. No native API found. Licence: not found.
- data.un.org (UN System Data Commons) fetched empty; API and licence not established.
- UN website terms (un.org/en/about-us/terms-of-use): personal non-commercial use only. No resale, redistribution or derivative works unless material-specific terms say otherwise.

Gaps: no open, cross-domain (democracy plus rights plus conflict) live dashboard with a documented API. The expert surveys are US-only. Rights-violation event monitoring is thin.

## Evidence

- https://www.idea.int/democracytracker/ : monthly, 173 countries, no data terms
- https://www.v-dem.net/data/the-v-dem-dataset/ : v16, CC BY-SA 4.0
- https://brightlinewatch.org/ : Wave 29
- https://acleddata.com/conflict-alert-system/ : CAST, login required
- https://acleddata.com/terms-of-use/ : links to EULA and usage terms
- https://www.cfr.org/global-conflict-tracker : 27 conflicts
- https://viewsforecasting.org/ : monthly forecasts, open access
- https://github.com/prio-data : repo list
- https://www.mediacloud.org/ : consortium, open source
- https://api.github.com/repos/<owner>/<repo> : stars and dates above
- https://www.un.org/en/about-us/terms-of-use : UN reuse terms
- https://centre.humdata.org/un-peace-and-security-data-on-hdx/ : search snippet only; HDX mirror and API

## Caveats (verbatim)

ICG, Liveuamap, the Protect Democracy index page and the ACLED terms documents were not read. The psdata and data.un.org content was not rendered. Section 3 is from memory. Wikipedia licence unverified.

## Orchestrator note

The gap statement is the one that justifies Canary: nothing open and cross-domain exists with a documented methodology and evidence trail, the monthly curated trackers (IDEA, CrisisWatch) are human-written and not machine-readable, and the expert surveys that come closest to "early warning for democracy" are US-only. Reuse candidates: Media Cloud's fetcher stack, Bellingcat's auto-archiver (MIT) for preserving cited pages, and the ViEWS and EWP forecasts as external structural-risk inputs rather than something to rebuild.
