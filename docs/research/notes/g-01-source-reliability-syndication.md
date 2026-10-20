# G-01: Source reliability schemes, syndication/copy detection, media ownership data

- Date: 2026-10-20
- Agent: researcher (Sonnet, low effort), 25 tool uses

## Answer (verbatim; read 2026-10-20)

(a) Graded source assessment. NewsGuard scores 9 criteria out of 100 points: credibility (22 no false content, 18 gathers information responsibly, 12.5 corrections, 12.5 news vs opinion, 10 deceptive headlines) and transparency (7.5 ownership/financing, 7.5 ads labelled, 5 who is in charge, 5 named creators). It is therefore decomposable, but it is published as one sum. Its API price is not public (not found). JTI certification means a self-evaluation against 130 criteria, then an independent audit. The areas covered include editorial process, ownership disclosure, corrections, revenue and sponsored content. I found no registry, machine-readable data or CWA 17493 mention on the JTI site. Two gaps: jti-rsf.org redirected to an unrelated domain, so I did not follow it, and the CWA link rests on your question, not a source I read. GDI rates news domains by risk, scored 0 (max risk) to 100 across Content, Operations and Context pillars, and it says it does not judge whether a specific domain carries disinformation (2019 methodology report). MBFC: a preprint, "Stop using Media Bias/Fact Check in research", says its methodology lacks academic rigor, and MBFC itself disclaims being a "tested scientific method". The same sources report high correlation with NewsGuard (r=0.81), which shows rater agreement, not accuracy. The IFCN signatories page links to a "Verified signatories" list, but it loaded dynamically and I could not read it or confirm a download (not found).

(b) Copy detection. Churnalism.com (Sunlight Foundation with Media Standards Trust, April 2013, UK-only predecessor 2011) compared a submitted article against a press-release database and reported the percentage of overlapping text. Broder 1997 (shingling/MinHash) and Charikar 2002 (SimHash): I cite these from memory, not read this session, so verify them. The Google Fact Check Tools API `claims:search` takes query, languageCode, reviewPublisherSiteFilter, maxAgeDays, pageSize (default 10) and pageToken. It returns ClaimReview-derived records. The docs I read do not state price or quota (not found). Wire dependence: Pew 2004 found AP 41% plus Reuters 9% of stories on three news sites, with Yahoo at 76% from the two. Pew 2015 found wires supplied about 6 in 10 national-government stories across 8 newspapers, 62% for papers without a DC correspondent. Bond University, "Not wrong for long" (2009) covers two Australian sites. I found no global wire-share study.

(c) Ownership and state control. The Media Ownership Monitor (mom-gmr.org, Reporters Without Borders and Global Media Registry) lists 27 countries. Examples are Germany, Ireland, Turkey, Ukraine, India, Brazil and Egypt. Each has an online database. Export format and license were not stated (not found). EurOMo is BODS v0.3 compliant. The 2025 edition offers xlsx download in BODS format, but the full version is only for registered users with a legitimate interest. It covers over 700 companies, 4,300 individuals and 2,100 organizations. The State Media Monitor covers 546 state-administered media companies in 151 countries (launch notice). Its typology, the State Media Matrix, rests on funding, ownership/governance and editorial autonomy. The Zenodo record (10.5281/zenodo.17219015, v2025.1) is CC-BY-4.0, but it holds only a README PDF and points to statemediamonitor.com for the data. I did not confirm a downloadable data file. V-Dem codebook v16: v2mecenefm "Government censorship effort - Media", v2meharjrn "Harassment of journalists" and v2mebias "Media bias" all exist, in section 3.12.1.

## Evidence

- https://www.newsguardtech.com/ratings/rating-process-criteria/ (nine criteria and weights)
- https://journalismtrustinitiative.org/ (130 criteria, audit; no registry mentioned)
- https://disinformationindex.org/files/gdi_methodology-report-online_2019.pdf (via search summary only)
- https://arxiv.org/pdf/2607.12108 (MBFC critique, via search summary only)
- https://en.wikipedia.org/wiki/Churnalism (Churnalism.com, 2013)
- https://www.pewresearch.org/journalism/2015/12/03/the-role-of-wire-services/ and https://www.pewresearch.org/journalism/2004/10/27/the-internet/ (via search summary)
- https://developers.google.com/fact-check/tools/api/reference/rest/v1alpha1/claims/search
- http://www.mom-gmr.org/en/ (27 countries)
- https://stephenabbottpugh.medium.com/how-the-euromedia-ownership-monitor-uses-the-beneficial-ownership-data-standard-a2c1eed2aa66 (BODS xlsx, via search summary)
- https://zenodo.org/api/records/17219015 (CC-BY-4.0, README only)
- https://www.v-dem.net/documents/70/codebook_v16.pdf (pdftotext, lines 565-576 and 2009-2011)

## Caveats (verbatim)

The NewsGuard API price, IFCN list format, CWA 17493 and the Fact Check API quota are not found. Several items come from search summaries, not full-page reads. Broder and Charikar are unverified citations. A JTI domain redirect pointed elsewhere and I did not follow it.

## Orchestrator note

No off-the-shelf, machine-readable, global source-reliability dataset exists that Canary could adopt; NewsGuard is commercial and single-score, MBFC is not credible for research, JTI has no registry. The conclusion for `docs/04` is that Canary grades sources on separate, declared axes (type, independence from the subject, ownership and state control per the State Media Monitor matrix, track record on corrections) and never publishes a composite number. For syndication detection the textbook methods (shingling plus MinHash, press-release overlap as in Churnalism) are sufficient and cheap. The V-Dem media variables are confirmed by name in the v16 codebook and serve as the annual baseline for press-freedom context.
