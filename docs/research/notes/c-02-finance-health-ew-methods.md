# C-02: Early-warning methods from financial-crisis research and public-health surveillance

- Date: 2026-10-20
- Agent: researcher (Sonnet, low effort), 13 tool uses
- Coverage: partial; several primary PDFs were unreadable (see caveats)

## Answer (verbatim; read 2026-10-20)

1. Signals approach. Each indicator is monitored, and when it crosses a threshold that is read as a signal that a crisis may occur "within the following 24 months" (IMF abstract, confirmed). Thresholds are chosen per indicator to minimise the noise-to-signal ratio, and the composite index weights indicators by inverse NSR. These two points come from secondary reviews (arXiv 2010.10132), not the paper's text. The abstract names the best indicators: exports, real exchange rate deviation from trend, M2/reserves, output, equity prices. In-sample and out-of-sample hit and false-alarm figures: not found. The paper PDF and the 1999 AER "Twin Crises" paper were not retrieved. Berg and Pattillo 1999 was not retrieved either, so I can say nothing sourced about it.
   Later assessment: Drehmann and Juselius (BIS WP 421, 2013; IJF 2014) judge indicators against policymakers' decision needs. They find the credit-to-GDP gap and the debt service ratio "consistently outperform other measures". The gap works best at longer horizons and the DSR at shorter ones (BIS abstract, confirmed). Loss-function details were not read.

2. Aberration detection. The `surveillance` vignette (Salmon, Schumacher and Höhle, "Monitoring Count Time Series in R", CRAN) covers earsC1/C2/C3, farrington, farringtonFlexible and cusum. Its text was unreadable (binary PDF), so assumptions and false-alarm behaviour are not found. Noufaily et al. 2013 (Stat Med) was not retrieved. Background knowledge, unverified: EARS uses a moving baseline mean and SD with a threshold. Farrington fits an overdispersed Poisson GLM with trend and seasonality. Noufaily's revision reweights the baseline and adjusts the threshold, with the aim of reducing false positives.

3. Open-source epidemic intelligence. The WHO EIOS page says EIOS analyses open-source data "in near real time" and that experts across organisations detect, contextualise, analyse, assess and share information. It says nothing on verification, duplicates or noise, and it disclaims any accuracy guarantee. Freifeld et al. 2008 (JAMIA 15(2):150-157) describe HealthMap. It ingests Google News, ProMED Mail and validated official alerts, and a text classifier assigns disease and location. Staff curate all reports daily to correct misclassifications, and the pattern dictionary is updated daily. The paper has no separate verification step: reliability is inherited from the source (ProMED is expert-curated, and official alerts such as WHO announcements are called "validated"). Duplicate clustering is listed as future work. Unclassified items include non-disease news that slipped through the filter. Classifier accuracy over 10 Oct to 9 Nov 2007 was 655 of 778 reports (84%): ProMED 91%, Google News 81%. This measures classification correctness, not signal-to-noise or false alarms. ProMED and GPHIN published descriptions, and the EIOS "signal/event/verified" taxonomy: not found.

## Evidence

- https://www.imf.org/external/Pubs/FT/staffp/1998/03-98/kaminsky.htm — KLR abstract: 24-month signal, best indicators.
- https://arxiv.org/pdf/2010.10132 — secondary review (from search snippet only): the noise-to-signal minimising threshold and inverse-NSR weighting.
- https://www.bis.org/publ/work421.pdf — Drehmann and Juselius: credit gap and DSR best, by horizon.
- https://cran.r-project.org/web/packages/surveillance/vignettes/monitoringCounts.pdf — title and authors only.
- https://www.who.int/initiatives/eios — EIOS overview, little method detail.
- https://pmc.ncbi.nlm.nih.gov/articles/PMC2274789 — Freifeld 2008 full text, read.
- https://pubmed.ncbi.nlm.nih.gov/18096908 — PubMed record, listed in search results but not opened.

## Caveats (verbatim)

Fetch failures were the IMF WP9807 PDF (redirected to a 404), the IMF Leading Indicators working-paper page (404), the PubMed page for Noufaily (cookie wall) and the surveillance vignette (binary PDF). False-alarm rates for the signals approach, EARS/Farrington/CUSUM and GPHIN/EIOS are therefore not found from primary text. Needed next: the KLR and Kaminsky-Reinhart PDFs, Berg and Pattillo, Noufaily 2013, the surveillance reference manual, the EIOS Strategy 2024-26, and a GPHIN paper.

## Orchestrator note

What transfers is structural, not numerical: (1) the signals approach's discipline of choosing an indicator threshold by its historical noise-to-signal ratio and declaring a fixed signalling window; (2) the surveillance-statistics practice of modelling an expected count with trend and seasonality and flagging exceedances, with the known false-alarm cost of rising reporting volume; (3) HealthMap's design, in which classification is automated but every report is curated by staff daily and reliability is inherited from the source rather than computed. The specific false-alarm figures remain to be read from the primary papers before any number is quoted.
