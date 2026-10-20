# F-07: Governmental and intergovernmental conflict early-warning systems

- Date: 2026-10-20
- Agent: researcher (Sonnet, low effort), 27 tool uses

## Answer (verbatim; read 2026-10-20; many primary pages were unreadable, so gaps are marked "not found")

1. EU GCRI (JRC). A quantitative model estimating the probability and intensity (battle deaths) of violent conflict in about 140 countries, 1-4 years ahead. It uses 22 open-source variables across six dimensions: social, economic, security, political, geographic/environmental, demographic. The current method is "GCRI 2022: Revised Data and Methods", JRC131326, 7 Dec 2022. It compared 14 models, reports improved predictive performance, and discusses limitations. Download link, licence and update cadence: not found. The DRMKC page and the science4peace page returned 404, a login page, or a redirect. The JRC record gives conflicting access statements and names no licence. Older JRC reports say reuse is under Commission Decision 2011/833/EU. EEAS Conflict Early Warning System: not read from an EEAS page; my understanding is that it is an internal EEAS/Commission risk-assessment process that uses GCRI as an input, and it has no public product (unverified). Critique: only the JRC's own statement that the 2022 revision improved performance; no independent evaluation found.

2. Germany PREVIEW (Auswärtiges Amt). Data-driven crisis early-warning and information-management project. The Foreign Office has a scientific advisory board for it. A 2020 ministry briefing (FOI release) describes graphics, maps, dashboards and ML forecasts. The target variable is mainly conflict deaths, and the tool does not use causal models. It draws on public sources and social media. In 2021 it was linked with the Bundeswehr's early-warning system. Public output: nothing found; the briefing came through an FOI request. No API or licence found. Effectiveness assessment: not found.

3. African systems.
- AU CEWS (Situation Room): gather, analyse and alert on threats. Public outputs: not found, apart from PSC communiqués. A PSC communiqué of 24 Aug 2026 covers validation of a Continental Threats Assessment and Risks Mapping Tool. A PSC communiqué (COMM.1208, April 2024) addresses obstacles to effective CEWS. Assessment: Engel 2018, South African Journal of International Affairs, on AU knowledge production and CEWS limits (snippet only).
- ECOWARN (ECOWAS Early Warning Directorate): collects open-source data on human-security indicators and reports to the Commission President. Public reports or data: not found. Assessment: a 2012 fieldwork study, seen only via search snippet, cites staff shortages, weak collection methods, bureaucracy and reluctance to act on recommendations.
- IGAD CEWARN (cewarn.org): public early warning reports, alerts, baseline and country reports, special reports, monthly alerts, the protocol, and a book, "Conflict Early Warning in the Horn: CEWARN's Journey". No raw dataset is listed.
- Comparative assessment: Wulf and Debiel 2009, LSE CSRC Working Paper 49. I read only the abstract, not the findings.

4. UN. "Regional Monthly Review": not found in any public source. Treat it as internal. Horizon-scanning briefings to the Security Council are documented as having stopped after 2012 (Security Council Report). The Framework of Analysis for Atrocity Crimes (OSAPG, 2014) is public: common and specific risk factors with indicators, transmitted as A/70/741-S/2016/71. A 2021 SG R2P report calls it useful for structural risk factors. Case-level analyses made with it are not public.

5. US. The Elie Wiesel Act (S.1158, 2018) requires annual reports to Congress. The first came Sept 2019, 61 days late, with a classified annex. It launched the interagency Atrocity Early Warning Task Force (NSC, State, DoD, DHS, DOJ, Treasury, USAID, Intelligence Community). The public reports give an overview of prevention efforts: assistance, diplomacy, multilateral action, training. Per civil-society assessments, they do not publicly name at-risk countries. The Alliance for Peacebuilding's PPWG assessments of the 2020 and 2021 reports make that critique, but I could not read the PDFs. The Early Warning Project (USHMM Simon-Skjodt Center with Dartmouth's Dickey Center) publishes a statistical risk assessment of more than 160 countries. Its downloads page offers an R file, a data dictionary and a GitHub link, labelled 2023-24. The latest report seen is 2025-26. Licence: not found.

6. Warning-response literature. George and Holl 1997, Carnegie Corporation, May 1997, argue that warning must induce action and that leaders postpone hard choices. Wulf and Debiel 2009, LSE CSRC WP49, compare early warning and response mechanisms across AU, ECOWAS, IGAD, ASEAN/ARF and PIF.

## Evidence

- https://publications.jrc.ec.europa.eu/repository/handle/JRC131326 — GCRI 2022 abstract; no licence or data link
- https://www.cewarn.org — list of CEWARN publications
- https://researchonline.lse.ac.uk/id/eprint/28495/ — Wulf and Debiel abstract
- https://carnegie.org/publication/the-warning-response-problem-and-missed-opportunities-in-preventive-diplomacy/ — George and Holl 1997
- https://earlywarningproject.ushmm.org/downloads — EWP files (search snippet; fetch failed)
- https://asil.org/node/12035 — first Wiesel report, classified annex (snippet)
- https://www.securitycouncilreport.org/monthly-forecast/2013-05/in_hindsight_horizon_scanning_briefings.php — horizon scanning ended after 2012 (snippet)
- https://documents.un.org/doc/undoc/gen/n16/042/32/pdf/n1604232.pdf — Framework of Analysis (snippet)
- https://media.frag-den-staat.de/files/foi/530924/20200929_BS_KIWS_PREVIEWfinFIFG_geschwaerzt.pdf — PREVIEW briefing (snippet only)

## Caveats (verbatim)

Most "read" items come from search summaries or abstracts. The PDFs for the LSE paper, the PPWG assessment, the ISS brief and the GCRI report were binary and unreadable. The DRMKC and science4peace pages did not load. The EEAS system and the AU and ECOWARN publication claims are unverified.

## Orchestrator note

The pattern across governments is consistent: early-warning systems exist, their outputs are internal or classified, and the published critiques concern response, not detection. This is the gap a public, evidence-showing system can fill without competing with them: Canary does not need to out-forecast PREVIEW; it needs to make the public evidence legible.
