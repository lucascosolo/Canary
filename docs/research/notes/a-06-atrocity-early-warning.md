# A-06: USHMM Early Warning Project, PITF Problem Set, UN Framework of Analysis for Atrocity Crimes

- Date: 2026-10-20
- Agent: researcher (Sonnet, low effort), 24 tool uses

## Answer (verbatim)

1. EWP (read 2026-10-20). Annual Statistical Risk Assessment (SRA) ranks "more than 160" countries by estimated risk of a new onset of intrastate mass killing. The site headline says "state- or nonstate-led", and the methodology page says episodes are coded 1960-present for state-led and 1989-present for nonstate-led, so the "state-led only" framing is outdated. The latest is 2025-26. The summary handout is dated 15 Dec 2025, and the site's ranking page says "risk for onset ... in 2025-26"; top 30 = "high risk". Method: logistic regression with elastic-net regularization, trained on 1960-2015 data, forecasting two years ahead. It uses 38 variables from about a dozen sources, in five groups: basic country characteristics, war and conflict, human rights and civil liberties, governance, socioeconomic. The ones I saw: infant mortality, new-country flag, years since independence, population, region dummies, coup attempts in past 5 years, any mass killing since 1945, average annual onset rate, battle-related deaths, onset in prior year, number of ongoing mass killings. The full list is on /methodology-risk-factors; I did not capture the rest. A Data Dictionary is downloadable. The CSV "All 2025-26 Data" is at /api/sra/download/csv/2026-sra (HTTP 200). All source data are on GitHub (github.com/earlywarningproject). An Accuracy page with sensitivity/precision metrics (analysis done in 2025) is published, and the site notes a base rate of about 1% of countries per year. Whether model code is published: not confirmed (GitHub holds data; I did not open the repo). Terms: the site links to the USHMM general Terms of Use; I did not read them, so the data licence is not found.

2. PITF Problem Set (read 2026-10-20 via systemicpeace.org/inscrdata.html, summarised by fetch tool). Four event types: ethnic war, revolutionary war, adverse regime change, genocide/politicide. Coverage 1955-2018; latest update 2018. Formats: Excel, plus PDF table and codebook. Terms: CSP holds copyright; citation is required; redistribution needs prior written permission.

3. UN Framework (read 2026-10-20). The PDF is "United Nations, 2014 (reprinted in 2018)". It has 14 risk factors, the first 8 common and 6 specific (2 per crime). The Framework calls itself "a public document". Common: (1) situations of armed conflict or other forms of instability; (2) record of serious violations of international human rights and humanitarian law; (3) weakness of State structures; (4) motives or incentives; (5) capacity to commit atrocity crimes; (6) absence of mitigating factors; (7) enabling circumstances or preparatory action; (8) triggering factors. Specific: genocide (9) intergroup tensions or patterns of discrimination against protected groups, (10) signs of intent to destroy a protected group in whole or in part; crimes against humanity (11) signs of a widespread or systematic attack against a civilian population, (12) signs of a plan or policy to attack a civilian population; war crimes (13) serious threats to those protected under IHL, (14) serious threats to humanitarian or peacekeeping operations. Ongoing country-level indicator data: none found. It is a qualitative analyst tool; the Office's assessments are not published.

## Evidence

- https://earlywarningproject.ushmm.org/statistical-risk-assessment — 160+ countries, 2025-26, CSV link, GitHub, accuracy
- https://earlywarningproject.ushmm.org/methodology-statistical-model and /methodology-risk-factors — method, 38 variables
- https://earlywarningproject.ushmm.org/accuracy
- https://www.systemicpeace.org/inscrdata.html
- https://static.un.org/en/preventgenocide/rwanda/assets/pdf/Guidance-Genocide_Framework%20of%20Analysis-English.pdf — official PDF; the 8+6 split and the "public document" wording confirmed on pp. 5-6

## Caveats (verbatim)

The 14 factor names are from my memory of the Framework, NOT verified against the PDF pages I read (the factor pages did not render). Check them against the PDF before citing. The official un.org PDF URLs I tried returned 404; the static.un.org copy works. PITF facts come from the fetch tool's summary, not a raw page read. The 2018 PITF end year seems stale for Oct 2026, so check for a newer file. EWP data licence, model-code availability and the full variable list: not confirmed.

## Orchestrator note

The EWP's published base rate (about 1% of countries per year) and its public accuracy page are the anchor for any probability language this project uses about mass killing: a country-year forecast is dominated by the base rate, and any UI copy must say so. The 14-factor list is to be checked against the PDF before it is embedded in the analytical framework.
