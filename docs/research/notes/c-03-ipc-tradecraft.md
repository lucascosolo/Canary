# C-03: IPC/FEWS NET protocols, Admiralty grading, Berkeley Protocol, structured analytic techniques

- Date: 2026-10-20
- Agent: researcher (Sonnet, low effort), 33 tool uses

## Answer (verbatim; read 2026-10-20)

Blocks 2 and 3 are mostly confirmed against primary documents. Block 1 (IPC Manual 3.1) is NOT established: ipcinfo.org and PDF mirrors returned HTTP 403.

1. IPC 3.1 and FEWS NET: "not found" for the specifics (phases, convergence of evidence, reliability scoring and minimum evidence, confidence levels with asterisks, current vs projection).
- Recalled from memory, unverified: five phases are Minimal/None, Stressed, Crisis, Emergency, Catastrophe/Famine; confidence is Low/Medium/High shown as asterisks.
- Search summaries say 3.1 is the current version, and that v2.0 (2013) set a minimum evidence base of at least one reliable piece of evidence per outcome plus several across contributing factors. Whether 3.1 kept this is unverified.
- FEWS NET scenario development (from the guidance page summary only): an eight-step process. It sets assumptions about key shocks, traces their effect on food and income sources, weighs actor responses, and produces a "most likely" scenario classified on the IPC scale.

2. Admiralty system, from a secondary reproduction. NATO AJP-2.1 and STANAG 2511 text was not found, and the doctrine is not public.
- Reliability: A completely dependable; B usually dependable; C fairly dependable; D not usually dependable; E unreliable; F cannot be judged.
- Credibility: 1 confirmed by other sources; 2 probably true; 3 possibly true; 4 doubtful; 5 improbable; 6 truth cannot be judged.
- Berkeley Protocol: launched 1 Dec 2020 by OHCHR and UC Berkeley Human Rights Center; a UN library record dates the UN edition 2022. It sets "minimum professional standards" for identification, collection, preservation, verification and analysis of digital open-source information. Its specific chain-of-custody requirements were not read.

3. Structured analytic techniques
- ICD 203 (signed 2 Jan 2015, amended 2022 and 2023), read at section D.6.e(2)(a), with ranges. Terms must come from one row.
  - almost no chance / remote: 01-05%
  - very unlikely / highly improbable: 05-20%
  - unlikely / improbable: 20-45%
  - roughly even chance / odds: 45-55%
  - likely / probable: 55-80%
  - very likely / highly probable: 80-95%
  - almost certain / nearly certain: 95-99%
  - ICD 203 also bars combining a confidence level and a likelihood term in one sentence.
- IPCC guidance note (Mastrandrea et al. 2010, AR5 version), read directly.
  - Likelihood: virtually certain 99-100; very likely 90-100; likely 66-100; about as likely as not 33-66; unlikely 0-33; very unlikely 0-10; exceptionally unlikely 0-1.
  - Confidence: very low, low, medium, high, very high, set from evidence (limited/medium/robust) and agreement (low/medium/high).
- Heuer ACH: Chapter 8 exists, and Step 3 is the hypotheses-by-evidence matrix with diagnosticity (book pp. 100-101). The other steps were not read in the source. The conventional list is: hypotheses; evidence; matrix; refine; tentative conclusions; sensitivity; report; milestones.
- Sherman Kent's Words of Estimative Probability: not found.
- Grabo, Anticipating Surprise (JMIC, Dec 2002): not read. A secondary source says her indicator lists date from the early 1950s and list actions an adversary must take before hostilities.

## Evidence

- https://archive.dni.gov/files/documents/ICD/ICD-203.pdf: probability table, read directly.
- https://www.stat.berkeley.edu/users/aldous/157/Papers/ipcc_uncertainty-guidance-note.pdf: IPCC likelihood and confidence scales, read directly via a mirror. The canonical URL https://www.ipcc.ch/site/assets/uploads/2017/08/AR5_Uncertainty_Guidance_Note.pdf returned 403.
- https://www.cia.gov/resources/csi/static/Pyschology-of-Intelligence-Analysis.pdf: Heuer, Step 3 pages only.
- https://eugit.opencloud.lu/MISP/misp-taxonomies/raw/tag/rm/admiralty-scale/README.md: Admiralty definitions (secondary).
- https://humanrights.berkeley.edu/projects/berkeley-protocol-on-digital-open-source-investigations/: Berkeley Protocol scope and date.
- https://fews.net/global/guidance-documents/january-2018: FEWS NET scenario development (summary only).
- Targets that were not readable (403 or binary): https://www.ipcinfo.org/ipc-manual-interactive/en/ ; https://fscluster.org/sites/default/files/documents/ipc_technical_manual_3_final.pdf ; https://www.ohchr.org/sites/default/files/2024-01/OHCHR_BerkeleyProtocol.pdf ; https://apps.dtic.mil/sti/pdfs/ADA476752.pdf (Grabo).

## Caveats (verbatim)

IPC 3.1 details, the Admiralty primary doctrine, Berkeley chain-of-custody detail, Kent and Grabo text are unverified. IPC 3.1 needs a re-read via a non-blocked route. Admiralty wording varies slightly between sources.

## Orchestrator note

Three things are adopted from this note. The IPCC's two-axis scheme (evidence: limited/medium/robust; agreement: low/medium/high; confidence derived from both) is the model for Canary's confidence labels because it keeps "how much evidence" and "do sources agree" separate, which START.md section 6 demands. The ICD 203 rule that a likelihood term and a confidence level never share a sentence becomes a UI copy rule. The Admiralty two-axis grading (source reliability, information credibility) is the model for per-claim evidence records. The IPC manual is to be read through the browser in a later session.
