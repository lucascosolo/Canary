# 03. Data source catalog

Every source below was checked on 2026-10-20 against its own pages by a researcher agent; the
note in the last column holds the URLs, the date and the agent's caveats. "Licence for Canary"
answers one question: may a free, public, non-commercial site store the data, display it, and let
readers download what it shows? Values: **open** (yes, with attribution), **display** (show
unchanged with attribution; no derived redistribution), **links** (link and cite; do not store
beyond metadata), **permission** (written permission needed first), **excluded** (terms forbid the
use), **unverified** (terms not readable from here; treat as links until read). Priority: **P0**
first integration (Phases 0-1), **P1** Phases 2-3, **P2** later or conditional, **lead** unverified
suggestion.

## 1. Baseline indices (annual or slower)

| Source | What it gives Canary | Coverage | Cadence | Access | Licence for Canary | Limits | Priority | Note |
|---|---|---|---|---|---|---|---|---|
| V-Dem Country-Year v16 | Democracy, judicial constraints, media, civil liberties indices; the baseline layer's spine | 202 units, to 1789 | Annual, March | Direct ZIP/CSV, no registration; R package | open (CC BY-SA 4.0) | Expert-coded; one-year lag; uncertainty intervals should be shown | P0 | A-01 |
| V-Dem ERT v16 | Episode list for the historical library and for backtests | 1900- | Annual | GitHub, CSV | open (inherits V-Dem) | Codebook variables to confirm | P0 | A-01, G-04 |
| V-Dem V-Party v2 | Anti-pluralism index per party (`v2xpa_antiplural`) | 169 countries to 2019 (conflicting statements) | Irregular | CSV | unverified (codebook says all rights reserved) | Ends 2019; newer version to check | P1 | E-02 |
| Freedom House FIW/FOTN/NIT | Political rights, civil liberties, internet freedom; a second expert view | 195+13 / 72 / 29 | Annual | xlsx, some by request | display (non-profit use with citation; commercial needs approval) | No API; request flow unverified | P1 | A-02 |
| International IDEA GSoD | 30 indices in four categories | 174 countries, 1975- | Annual | Download from site | unverified | Half built on V-Dem (not independent) | P1 | A-02 |
| BTI 2026 | Status and governance indices for transition countries | 137 | Biennial | xlsx | unverified | Not global | P2 | A-03 |
| EIU Democracy Index | Fifth expert view | 167 | Annual | PDF; data unverified | unverified (site unreachable from sandbox) | Likely proprietary | P2 | A-03 |
| Polity5 | Regime scores for backtests | 1800-2018 | Ended 2018 | xls | permission (CSP) | Not live; display forbidden | P2 (backtest only) | A-03 |
| RSF Press Freedom Index | Five press-freedom pillars | 180, 2002-2026 | Annual, April | CSV | unverified (no licence text found) | Method changed 2022 | P1 | A-04 |
| CIVICUS Monitor | Civic-space rating and watchlist | ~199 | Annual rating (Dec); watchlist several times a year | Download | unverified (site CC BY-SA; data unclear) | No RSS/API for updates | P1 | A-04 |
| TI CPI 2025 | Corruption perception | 182, 1995- | Annual, Feb | xlsx | display (CC BY-ND; no derivatives) | Comparable from 2012 only; perception-based | P1 | A-05 |
| WGI 2026 | Six governance aggregates | ~200, 1996-2025 | Annual | xlsx/Stata | display (usage advisory, no licence) | Recalculated history in 2025 | P1 | C-01 |
| PTS 2026 | State repression scale from Amnesty/State/HRW reports | 1976-2025 | Annual, Sept | csv | unverified (no licence stated) | Three overlapping series | P1 | E-03 |
| CIRIGHTS | Disaggregated rights scores | ~40 years | Annual | xlsx/dta | unverified | Citation required | P2 | E-03 |
| HRMI Rights Tracker | Civil/political (survey) and economic/social (stats) rights | Partial | Annual | Download | display (CC BY-NC; embargoed page says CC BY) | Licence conflict to resolve | P1 | E-03 |
| Academic Freedom Index 2026 | Academic freedom, from V-Dem data | 179 | Annual | PDF + V-Dem data | open (via V-Dem) | — | P1 | E-03 |
| EWP Statistical Risk Assessment 2025-26 | Published structural mass-killing risk with base rate and accuracy page | 160+ | Annual, Dec | CSV at /api/sra/download/csv/2026-sra; GitHub | unverified (USHMM terms; data on GitHub) | 1-2 onsets/year base rate; two-year horizon | P0 | A-06, G-03 |
| Fragile States Index | Fragility composite | 179, 2006-2023 online | Annual | xlsx | unverified | Methodological critique (Dev. and Change 2018); later years not listed | P2 | E-04 |
| Global Peace Index 2026 | Peace composite | 163 | Annual | PDF | unverified | No raw data found | P2 | E-04 |
| INFORM Risk Mid-2026 | Hazard, vulnerability, coping capacity | Global | Annual-ish | xlsx | unverified | Licence and API not found | P2 | B-06 |

## 2. Event and change sources (daily to monthly)

| Source | What it gives Canary | Coverage | Cadence | Access | Licence for Canary | Limits | Priority | Note |
|---|---|---|---|---|---|---|---|---|
| UCDP Candidate | Monthly organised-violence events | Global, 1989- | Monthly, ≤1 month lag | CSV; API with token (5,000/day) | open (CC BY 4.0) | 25-death threshold; media-dependent | P0 | B-02 |
| UCDP GED v26.1 / ACD | Annual georeferenced events; conflict-year data for backtests | 1989-2025 / 1946-2025 | Annual | ZIP/CSV | open (CC BY 4.0) | — | P0 | B-02 |
| GDELT 2.0 Events/GKG, DOC API | Attention volume, tone, themes, URLs in 65 translated languages | Global, 2015- (DOC: 2017-) | 15 min | Raw files; DOC API (250-article cap) | open (free for any use with citation) | Not an event record (≈1 in 5 protest events real in the 2016 test); duplication; English pivot | P0 (volume and URL discovery only) | B-03 |
| Cloudflare Radar outages | Internet outages incl. government-directed shutdowns | Global | Near real time | REST with free token | display (CC BY-NC 4.0) | Rate limits unstated | P0 | B-05 |
| OONI | Blocking measurements per network | Where probes run | Continuous | API, S3 | display (CC BY-NC-SA 4.0) | Volunteer-probe dependence | P1 | B-05 |
| Access Now #KeepItOn | Documented shutdowns since 2016 | Global | Annual with retroactive additions | Spreadsheet | unverified (site CC BY) | Fields not confirmed | P1 | B-05 |
| ReliefWeb API | Humanitarian reports and disaster records | Global | Continuous | REST, pre-approved appname, 1,000 calls/day | open for ReliefWeb content (CC BY 4.0); partner reports links | Body-text field to confirm | P0 | B-06 |
| HDX HAPI | Standardised humanitarian series | Partial | Varies | REST, app identifier, 1 req/s | unverified (per-dataset; ACLED-derived fields at risk) | Theme list to confirm | P1 | B-06 |
| ACAPS | Severity index, access, protection risks | Crisis countries | Varies | REST with token | unverified | — | P2 | B-06 |
| World Bank Indicators API | Macro and social series; food prices | Global | Quarterly WDI | REST, no key | open (CC BY 4.0 default; check per dataset) | No documented rate limit | P0 | C-01 |
| IMF Data (SDMX 3.0) | WEO, BOP, fiscal series | Global | Varies | SDMX; auth unconfirmed | display (non-commercial with attribution; commercial needs permission) | Legacy API retired Nov 2025 | P1 | C-01 |
| OECD SDMX | OECD-member series | 38+ | Varies | REST, no auth | unverified (rate-limit statements conflict) | — | P2 | C-01 |
| ILOSTAT | Labour series | Global | Varies | SDMX; bulk csv.gz | unverified | — | P2 | C-01 |
| Our World in Data | Curated series with upstream licence in metadata | Global | Varies | CSV per chart; Parquet catalog | open for OWID-produced (CC BY 4.0); upstream varies | APIs "under development" | P0 | C-01 |
| UNHCR Refugee Data Finder API | Refugees, asylum, IDPs (via IDMC), nowcasts | Global | Mid-year and annual | REST, no credentials | unverified (terms unreadable) | — | P1 | H-02 |
| IOM DTM API v3 | IDP figures | Crisis countries | Varies | Key via developer portal | permission (terms bar redistribution) | — | P2 | H-02 |
| IDMC GIDD/IDU | Internal displacement | Global | Annual + events | API (key process unconfirmed) | unverified | — | P2 | H-02 |
| OpenSanctions | Sanctions and PEP designations | Global | 4× daily | Bulk JSON/CSV; yente self-host | display (CC BY-NC 4.0) | — | P1 | A-05, E-04 |
| SIPRI arms transfers, milex | Arms flows, military spending | Global, 1950- | Annual, March | Query tool; xlsx unconfirmed | display within fair use (non-commercial, <10% of a dataset) | No mirroring | P1 | E-04 |
| Cline Center Coup d'État v2.2.2 | Coups, attempts, conspiracies 1945-early 2026 | Global | Irregular, ~annual | CSV, Illinois Data Bank | open (CC BY) | — | P0 | D-03 |
| ViEWS forecasts | Published conflict-fatality forecasts 1-36 months | Global country; grid for Africa/MENA | Monthly or quarterly | Dashboard; downloads; `views_api` | unverified (no licence stated) | Shown as external model only | P1 | B-02 |
| ElectionGuide | Election calendar and results | Global | Continuous | Credentials by request; no API | links/display (free non-commercial with attribution) | No export | P1 | E-02 |
| IPU Parline | Parliament composition and election results | 188 parliaments | Daily | Open data; API | unverified (CC licence variant unknown) | — | P1 | E-01, E-02 |
| NELDA v6 | Election conduct codes for backtests | 1945-2020 | Irregular | Download form | unverified | Ends 2020 | P2 (backtest) | E-02 |
| PopuList v4 | Party family classification, Europe | 31 countries, 1989-2026 | Irregular | CSV | unverified | Europe only | P2 | E-02 |

## 3. Documents, trackers and feeds (text sources for claim extraction)

| Source | What it gives Canary | Coverage | Cadence | Access | Licence for Canary | Limits | Priority | Note |
|---|---|---|---|---|---|---|---|---|
| Publisher RSS feeds (curated list, ~200 outlets across regions and languages) | Headlines, links, summaries for claim extraction | By curation | Continuous | RSS/Atom | links + short excerpts; article text fetched under each publisher's terms and robots.txt, stored as extracted claims with quoted spans only | Copyright; paywalls; feed churn | P0 | B-04, G-02 |
| Wire services (AP, Reuters, AFP) | Not integrated directly; detected as lineage origin | — | — | — | excluded as feeds | — | — | G-01 |
| Media Cloud API | Story search by national media collection; counts over time; URL discovery | 25,000+ sources | Continuous | API key | unverified (terms page not found) | Full text not returned | P1 | B-04 |
| HRW, Amnesty and other NGO RSS | Reports as documents; claims about abuses | Global | Continuous | RSS (HRW live; Amnesty 404 on checked URL) | links + excerpts (terms unverified) | Advocacy framing to label | P0 | E-03 |
| Law Library of Congress Global Legal Monitor | Curated legal developments by country | Global | Continuous | RSS (feed URLs to confirm) | open (US government work, inferred) | — | P0 | E-01 |
| ICNL Civic Freedom Monitor | Laws affecting association, assembly, expression | 64 countries + 8 bodies | Irregular | Web | links (licence not found) | No export | P1 | E-01 |
| Venice Commission opinions; CODICES | Constitutional-law opinions, case law | CoE members and more | Irregular | Web | links | No RSS/API found | P1 | E-01 |
| International IDEA Democracy Tracker | Monthly curated democracy events (reference, not feed) | 173 countries | Monthly | Web | links | No data access | P1 (as comparator) | A-02, F-06 |
| Crisis Group CrisisWatch | Monthly conflict digest (reference) | ~70 countries | Monthly | Web (blocked from sandbox) | unverified | — | P1 (as comparator) | E-04 |
| Security Council Report monthly forecast | UNSC agenda context | — | Monthly | Web; RSS unconfirmed | links | — | P2 | E-04 |
| UN News, UN Press | Statements, briefings | — | Continuous | RSS (URLs to confirm) | links + excerpts (news material usable with credit) | General UN terms are restrictive | P1 | E-03, E-04 |
| OHCHR Special Procedures communications | Allegation letters and replies | Global | Continuous | Site states API and RSS exist | links | Endpoints unconfirmed | P1 | E-03 |
| ICJ, ICC | Case documents, press releases | — | Irregular | Web; ICJ RSS exists | links | ICC blocked from sandbox | P2 | H-01 |
| Global Centre for R2P Atrocity Alert | Weekly atrocity-risk bulletin | ~15-20 situations | Weekly | Web | links | RSS not found | P1 | H-01 |
| Election observation reports (ODIHR, Carter Center, EU EOM, OAS) | Executive summaries for claims about election integrity | Where missions deploy | Per election | Web/PDF | links + excerpts | No feeds found | P1 | E-02 |
| National legislative APIs (Congress.gov, UK Parliament, EUR-Lex, Bundestag DIP, Assemblée, Câmara) | Bill lifecycle for the policy tracker | Six jurisdictions | Continuous | REST/SPARQL; keys vary | open or display (varies; Etalab, EU reuse, UK OPL to confirm) | No equivalent for most countries | P2 | E-01 |
| Common Crawl CC-NEWS | Historical article corpus for backtests | 2016- | Daily | S3 WARC | unverified (copyright risk on user) | Not for display | P2 (backtests, after legal review) | B-04 |
| Internet Archive availability/CDX; Bellingcat auto-archiver | Preserve every cited page at citation time | — | On demand | REST | open | Rate limits unstated | P0 | H-01, F-06 |

## 4. Reference data

| Source | Role | Licence for Canary | Priority | Note |
|---|---|---|---|---|
| GeoNames daily dump | Gazetteer for toponym resolution (with `mordecai3`) | open (CC BY) | P0 | A-05, F-02 |
| Wikidata | Entity identifiers for actors, parties, institutions; election cross-checks | open (CC0) | P0 | A-05 |
| Natural Earth | Country and admin boundaries for the tile-free map | open (public domain) | P0 | A-05 |
| ISO 3166, M49 regions | Country codes and regional groupings | open | P0 | — |
| State Media Monitor | State-control classification of 546 outlets in 151 countries | unverified (Zenodo README CC BY; data on site) | P1 | G-01 |
| Media Ownership Monitor; EurOMo | Ownership records for 27 countries; EU BODS data | unverified / registered access | P2 | G-01 |
| OpenAlex | Scholarship on a country or episode, for the historical library | open (CC0) | P1 | H-01 |

## 5. Excluded or on hold, with the reason

| Source | Reason | Note |
|---|---|---|
| ACLED | EULA: non-commercial only, "own dashboard" not a permitted use, no direct access for others, AI/ML restriction regardless of purpose. Link only until ACLED's Access team confirms in writing what a public non-profit site may display. | B-01 |
| Global Terrorism Database | EULA bars public posting of data; organisational licence via CHC Global. | H-01 |
| Correlates of War | Non-commercial and no redistribution without written permission; usable for private backtests only. | H-01, G-04 |
| Manifesto Project | Scientific research only; no redistribution. | E-02 |
| Commercial news APIs (NewsAPI, GNews, NewsData) | No full-text redistribution rights at affordable tiers; terms bar public republication. | B-04 |
| UN documents in bulk | UN terms allow personal non-commercial use only; link and summarise in Canary's words. | E-03, E-04 |
| Survey microdata (WVS, ESS, barometers, ISSP) | Registration and non-redistribution terms; published aggregates may be shown after confirming each programme's reprint policy. | H-02 |
| US federal portals (user list) | US-specific; the catalog-as-discovery pattern is adopted; individual portals enter as leads when a US indicator needs them. | USER-01 |

## 6. First integration set (Phase 0 and 1)

Chosen for open licences, programmatic access without negotiation, and coverage of the three
layers in document 04:

1. **V-Dem v16 with ERT**: the baseline layer and the episode list. Annual; one adapter.
2. **UCDP Candidate (monthly) and GED/ACD (annual)**: the conflict-event layer, from the bulk
   CSV downloads only (CC BY 4.0, no token). The API, which needs a token by email, is not used.
3. **World Bank Indicators API and Our World in Data**: the economic and social context layer.
4. **EWP Statistical Risk Assessment CSV and Cline Center coups**: external structural risk and
   an outcome series for backtests.
5. **GDELT DOC API**: attention-volume time series per country and theme, and URL discovery for
   the news layer; never displayed as events.
6. **Cloudflare Radar outage annotations**: the first information-controls feed, using a token
   from the user's own existing Cloudflare account (no request to a third party; the user may
   strike this item, in which case OONI and #KeepItOn carry the role).
7. ReliefWeb is withdrawn: its API requires a pre-approved app name (B-06). Humanitarian
   context comes from the open datasets above and from NGO feeds under their own terms.
8. **A curated RSS list** of roughly 200 outlets and NGO feeds spanning every region and at least
   twelve languages, plus the Global Legal Monitor feed: the document layer for claim extraction.
   The list itself is a versioned file in the repository with a reason and a language for each
   entry, and it is the first thing the coverage index measures.
9. **Reference data**: GeoNames, Wikidata, Natural Earth, ISO codes.
10. **Archival**: Internet Archive availability check and save-on-cite.

Deferred to Phase 2-3: CIVICUS and RSF (licences to read; links until then), OpenSanctions bulk
files (no key, CC BY-NC), UNHCR (licence to read), OONI and #KeepItOn, SIPRI within its fair-use
clause, ViEWS (licence to read), the keyless legislative sources (EUR-Lex SPARQL, Brazil's Câmara
API, the French Assembly's open data). Withdrawn under the policy in section 8: Freedom House
(data by request), ElectionGuide (credentials), Media Cloud (account), IMF SDMX (auth
unconfirmed), IPU Parline's API (until confirmed keyless), Congress.gov and Bundestag DIP (keys),
HDX HAPI (app identifier), ACAPS (registration), IOM DTM, ReliefWeb.

## 7. The source registry

Every source, integrated or not, is a record in the registry (a versioned YAML directory in the
repository, loaded into the `source` table in document 08). Fields:

- identity: `id`, `name`, `organisation`, `homepage`, `type` (index, event_dataset, api,
  rss, document_feed, catalog, reference, model_output), `domains` (institutions, elections,
  legislation, conflict, rights, information, economy, humanitarian, reference), `countries`
  (ISO list or `global`), `languages`;
- cadence: `declared_cadence`, `expected_lag_days`, `revision_policy` (none, silent, announced);
- access: `access_method`, `endpoint`, `auth` (none, key, token_by_request, account, credentials
  by request), `rate_limit_text`, `adapter` (module name) ;
- terms: `licence_id` (SPDX where possible, else free text), `terms_url`, `terms_verified_on`,
  `canary_use` (open, display, links, permission, excluded, unverified), `attribution_text`
  (rendered wherever the source's data appears), `redistribution_notes`;
- independence: `source_class` (official_government, intergovernmental, ngo_advocacy,
  ngo_documentation, academic, media_wire, media_national, media_local, state_media, platform,
  model_output), `state_control_class` (from the State Media Monitor matrix where applicable),
  `funding_notes`;
- quality notes: free text on known biases, coverage gaps and methodological caveats, with
  citations; never a number;
- lifecycle: `status` (lead, evaluated, integrated, degraded, retired), `evaluated_on`,
  `integrated_on`, `retired_on`, `retired_reason`;
- health (runtime, in the database, not in YAML): last successful fetch, last change in schema,
  consecutive failures, items per day baseline, current items per day, freshness as shown to
  readers.

The registry is itself a public page (document 06): readers can see what Canary draws on, how
fresh each feed is, and what each licence permits. A source whose health check fails for longer
than its expected lag is shown as stale on every page that uses it, and the coverage index for
affected countries drops accordingly (document 04, section 6).

## 8. No-credentials, minimal-legal-risk policy (revision of 2026-10-20, afternoon)

The user's afternoon decision (DECISIONS.md) narrows the catalog. Rules applied from now on:

1. A source is integrated only if it is usable without registration, API key, token, account,
   credentials or written permission. Self-service keys from organisations other than the
   user's own existing accounts count as credentials and are not requested. The one standing
   exception is a token from the user's own Cloudflare account, which the user may withdraw.
2. A source is stored and displayed only if its licence is explicit and permits storage and
   display for personal non-commercial use (open, display with attribution, or CC BY-NC
   family). "Unverified" sources are links: title, URL and date only, no stored content.
3. News article text is kept for a configurable window (default 30 days) for re-processing and
   operator reading, then reduced to URL, title, publisher, date, language, content digest and the
   quoted passages behind each claim (size discipline for the utility VPS, revised 13:11 CDT).
   Open-licensed text is kept in full. Robots.txt and machine-readable reuse reservations are
   honoured; no paywall or login is circumvented; no site is fetched more often than once an
   hour per feed.
4. Datasets with "no redistribution" or "display unchanged only" terms (CPI, Polity, PITF, COW,
   GTD, SIPRI beyond fair use) are not mirrored. CPI is shown unchanged with attribution or linked.
5. Reuse of Common Crawl content is excluded (its terms place copyright risk and an AI-use
   indemnity on the user).
6. Every page carries attribution for every source it draws on, a disclaimer that the site is a
   personal, non-commercial tool presenting opinions based on cited public sources, and a
   contact address for corrections. Because access is controlled (user, 13:11 CDT), content
   rules beyond this are evidence standards (document 04, section 9), not legal minimisation.

Catalog consequences: P0 after revision is V-Dem (with ERT), UCDP bulk, World Bank, Our World in
Data, EWP SRA, Cline coups, GDELT (volume and URL discovery), Cloudflare Radar (conditional),
OONI, #KeepItOn, the curated RSS list, the Global Legal Monitor feed, reference data, and the
Internet Archive. Everything that needed a request is withdrawn or links-only as listed in
section 6.
