# A-03: EIU Democracy Index, Polity5, BTI

- Date: 2026-10-20
- Agent: researcher (Sonnet, low effort), 7 tool uses

## Answer (verbatim)

1. EIU Democracy Index: latest edition is 2025, released April 2026, covering 167 countries (press release via search; EIU's own pages could not be fetched, because eiu.com is blocked in this sandbox). Free country-score download: not found. Reuse and redistribution terms: not found. Paid data product and price: not found. I could not verify any of these from EIU. Third-party mirrors exist (Our World in Data grapher, Alphacast, an unofficial PDF upload on kverulant.org), but their licences are not EIU's. Treat redistribution in a dashboard as needing written EIU permission until you have read the terms.

2. Polity (CSP): Polity5 covers 1800-2018 (annual series 1946-2018, 167 countries with population over 500,000 in 2018). No post-2018 update is mentioned. The CSP Polity page says "PITF terminated its support for Polity in early 2020" and that "an improved and enhanced Polity5 version... is currently in development". No formal discontinuation or named successor is announced. Downloads are at systemicpeace.org/inscr/: p5v2018.xls and .sav (annual series), p5v2018d.xls and .sav (case format), and p5manualv2018.pdf. Terms: all resources are copyrighted by CSP. Citation is required, and reproducing or redistributing them needs prior written CSP permission, so a public dashboard that republishes scores needs that permission. The polity2 and PARCOMP definitions did not appear on the pages fetched. From the Polity5 manual as I recall it (not verified this session): polity2 is POLITY (DEMOC minus AUTOC, -10 to +10) with the -66/-77/-88 codes converted to usable values. PARCOMP is Competitiveness of Participation, a 0-5 scale from repressed through suppressed, factional, transitional and competitive. The "factional" level is a code within PARCOMP, not a separate factionalism variable. Confirm against the manual PDF.

3. BTI (Bertelsmann Stiftung): latest edition is BTI 2026; the cycle is every two years (2003 then 2006 onward, biennial). It measures whether developing and transition countries are moving toward democracy and a market economy. It has a Status Index (political and economic transformation) and a Governance Index (quality of political leadership). Coverage is 137 countries in 7 regional groups, developing and transition countries only (the methodology page says 137; I did not count the 2026 list). Data are free Excel (XLSX) files, plus Stata DTA for 2006-2022 and PDF codebooks, at bti-project.org/en/downloads. License and terms: not found. The pages fetched state no CC licence.

## Evidence (read 2026-10-20)

- https://www.systemicpeace.org/inscrdata.html — Polity5 1946-2018 and 1800-2018, download links, copyright and permission terms.
- https://www.systemicpeace.org/polityproject.html — PITF ended support in early 2020; improved Polity5 "in development"; 21-point scale.
- https://bti-project.org/en/downloads (first 100k of 235k characters) — BTI 2026 XLSX, multi-year XLSX, DTA, codebooks.
- https://bti-project.org/en/methodology — measurement concept, 137 countries, biennial.
- https://ourworldindata.org/grapher/democracy-index-eiu and the Cision press release at digital-release.kxan.com (search results only) — EIU 2025 edition, April 2026.

## Caveats (verbatim)

Every EIU field is unverified from primary sources. Check EIU's terms of use and its Democracy Index page from a machine that can reach eiu.com. The BTI license is unconfirmed; check bti-project.org imprint or terms, or ask Bertelsmann. A BTI download-page label ("2006-2022 Scores") mismatches its filename (2006-2024), and the multi-year XLSX is named 2006-2026. The Polity pages carry no visible update date.

## Orchestrator note

eiu.com being unreachable from the sandbox proxy is an environment limitation, not evidence about EIU. The Polity5 permission clause and the 2018 end of series together make Polity a historical-backtesting input only, not a live indicator.
