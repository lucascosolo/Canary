# B-01: ACLED access model and terms of use

- Date: 2026-10-20
- Agent: researcher (Sonnet, low effort), 13 tool uses

## Answer (verbatim)

As of 2026-10-20, ACLED data comes through a free myACLED account. The old API-key system was closed to new keys and kept running only until 15 September 2025. The API is now https://acleddata.com/api/ with an OAuth token (24-hour access token, 14-day refresh token) or cookie login. myACLED has four levels, Open, Research, Partner and Enterprise, set by your organisation. A generic email gets public (Open) access. From the FAQ table, my reading is Open = real-time data, Research = aggregated data (plus lagged event data), Partner = aggregated plus lagged event data, Enterprise = disaggregated weekly event data. Row limits, date windows and whether the full history is free were NOT FOUND on the pages I could read. The FAQ and API pages give none, and the only number is a default of 5000 rows per API call. The EULA (§3.1, §1.2) licenses non-commercial use only and says "Commercial entities may not access or use the Content and/or Platforms". A later commercial product therefore needs a separate licence from ACLED, and the FAQ lists "monetizing products created using ACLED's data" as a violation. Storing data in your own database is not explicitly addressed. EULA §3.1 says a licensee's "own dashboard" does not qualify as a permitted use. §3.3 bars letting others have "direct access to any of the Licensed Content", so redistributing raw data is out. External materials "must be transformative" so they "cannot be reverse engineered to recreate the Licensed Content". Aggregates are not explicitly addressed, but transformative aggregates are the safe path. Attribution: ACLED "must be clearly and prominently acknowledged". Cite the access date, the filters applied and any changes made, and put the citation on the visualization itself. Do not attribute your own analysis to ACLED. Coverage and cadence: the codebook says 6 event types and 25 sub-event types. Events are coded in real time and published weekly. A 2022 expansion made coverage global (confirmed), but the codebook gives no per-region start years. Sources are traditional media, international and NGO reports, local partner data and verified new media, in over 75 languages, with no crowdsourcing.

## Evidence (all read 2026-10-20)

- https://acleddata.com/api-documentation/getting-started — base "https://acleddata.com/api/"; POST https://acleddata.com/oauth/token (grant_type=password, client_id=acled, scope=authenticated); "default row limit of 5000"; no numeric rate limit.
- https://acleddata.com/myacled-faqs — four levels; "A member's level is determined by the organization they are associated with"; old keys end 15 Sep 2025; no row limits stated.
- https://acleddata.com/eula — §3.1, §1.2, §3.3 as quoted above.
- https://acleddata.com/contentusage — AI/ML restriction applies "regardless of whether such use is commercial, academic, or experimental"; must disclose how data were manipulated.
- https://acleddata.com/attributionpolicy — attribution rules as above.
- https://acleddata.com/methodology/acled-codebook — 6 types/25 sub-types, sources, 2022 global expansion, weekly publication. Fatality data are "typically the most biased and least accurate component of conflict reporting". Strategic developments are collected less systematically.
- https://acleddata.com/terms-of-use — only an index to the EULA, content usage terms and attribution policy.
- https://library.alnap.org/node/64946 — Eck 2012, Cooperation and Conflict 47(1), "In data we trust?": cautions that uneven quality control in ACLED can bias sub-national findings versus UCDP GED. From a search summary, not read in full.
- https://doaj.org/article/a9fe5df517e34e3288fefc54086af44f — Öberg and Yilmaz, Research & Politics 2025: dispute Raleigh, Kishi and Linke (Humanities & Social Sciences Communications), blaming ACLED/UCDP gaps on coding rules and source standards. From a search summary only.

## Caveats (verbatim)

No free-tier limits (rows, time window, full-history availability) were found. The tier-to-data mapping is inferred from a flattened FAQ table. The Raleigh/Kishi "2019" response was not verified and I cited the Linke paper instead. The academic citations come from search summaries. The EULA was summarised by a fetch tool, so check the §3.1 and §1.2 wording against the live page before relying on it. The https://acleddata.com/access-options URL returned 404, so check ACLED's access page or contact their Access team for tier limits and commercial licensing.

## Orchestrator note

Three clauses decide ACLED's role: a licensee's "own dashboard" is not a permitted use, commercial entities may not use the content at all, and the content-usage terms restrict AI/ML use regardless of purpose. Until the live EULA text is re-read and, if needed, ACLED's Access team has answered in writing, ACLED is classified as "not integrable" for Canary: UCDP, GDELT, and Canary's own extraction carry the conflict-event role, and ACLED appears only as an external link in the source registry.
