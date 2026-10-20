# B-03: GDELT access and weaknesses; POLECAT/PLOVER status

- Date: 2026-10-20
- Agent: researcher (Sonnet, low effort), 18 tool uses

## Answer (verbatim; read 2026-10-20)

1. GDELT. The GDELT 2.0 Event and GKG files update every 15 minutes, and the data page cites "65 live translated languages". The DOC 2.0 API is a full-text search of the last 3 months (the announcement says the index starts 1 Jan 2017). Timeline modes are TimelineVol, TimelineVolRaw, TimelineVolInfo, TimelineTone, TimelineLang and TimelineSourceCountry. ArtList MAXRECORDS defaults to 75 and caps at 250. Timeline steps are 15 min under 72 h, hourly up to 1 week, then daily. The minimum TIMESPAN is 15 min. The 65 languages are machine-translated into English and searched with English terms. The data page says all GDELT datasets are in BigQuery, but the dataset name "gdelt-bq", the lastupdate.txt URLs, the GEO 2.0 API details and the "please do not exceed N requests" guidance were not found in what I read. Article full text is not stated as provided. The only text-like field I saw was a 600-character contextual snippet in the Global Geographic Graph, so the expectation of URLs plus extracted fields is plausible but unconfirmed. Terms (about.html): "available for unlimited and unrestricted use for any academic, commercial, or governmental use of any kind without fee"; "any use or redistribution of the data must include a citation to the GDELT Project and a link to this website." No GDELT 3.0 announcement or 2025-26 outage notice was found; the search was shallow and the blog was not browsed.

2. Weaknesses. Wang, Kennedy, Lazer & Ramakrishnan (Science 353, 2016), from secondary summaries only: GDELT and ICEWS rarely reported the same Latin American protests; ICEWS and SPEED agreed on 10.3%; only 21% of GDELT-reported events referred to real protests; duplication from re-reporting; source corpus shifts over time. A 2025 J. Computational Social Science paper proposes automated GDELT deduplication (doi 10.1007/s42001-025-00409-4, title not read). Weller & McCubbins 2014, Ward et al. 2013 and Hammond & Weidmann 2014 were NOT verified; no 2020s geocoding error rate was found.

3. POLECAT. It is the ICEWS successor, coded by the NGEC machine-learning coder with PLOVER, which replaces CAMEO. Producers are the Program on Geostrategic Risk (formerly PITF); I found no Cline Center link, so that premise looks wrong. It is on Harvard Dataverse: "POLECAT Weekly Data", doi:10.7910/DVN/AJGVIT. It is CC0 1.0. Latest version is 62.0, released 2024-08-16 (Dataverse API on 2026-10-20), so nothing newer was visible, about 14 months stale. Files are yearly ngecEvents.DV.YYYY.txt up to 2024. The record says "updated hourly, and posted weekly", 7 languages, 1000+ sources, events from 2018 onward. The 2023 paper says it "will soon cover 2010-to-present", which conflicts with the 2018 start. Documentation is doi:10.7910/DVN/LMFPIP. A Schrodt deck says POLECAT replaces the PITF Dataverse ICEWS as of April 2023, and that source texts are not on Dataverse for IP reasons. ICEWS's exact last release date was not established. Reported accuracy in the Halterman et al. 2023 paper: 80-90% for event categories (about 10 points better than the comparison), and 89.27, 68.64, 71.19 and 69.49 for other tasks (the paper's footnote 16 says which; I did not map each figure), with a claim of exceeding human-coder teams.

## Evidence

- https://www.gdeltproject.org/data.html — 15-min updates, 65 languages, BigQuery
- https://www.gdeltproject.org/about.html — terms quoted above
- https://blog.gdeltproject.org/gdelt-doc-2-0-api-debuts/ — DOC API modes, 250 cap
- https://dataverse.harvard.edu/dataset.xhtml?persistentId=doi:10.7910/DVN/AJGVIT — POLECAT Weekly (via /api/datasets, v62.0, CC0)
- https://andrewhalterman.com/files/PLOVER_POLECAT_Halterman_Bagozzi_Beger_Schrodt_Scarborough.pdf — accuracy figures
- https://parusanalytics.com/eventdata/presentations.dir/Schrodt.PLOVER-PRIO.pdf — ICEWS replaced April 2023
- https://people.cs.vt.edu/~naren/papers/1502.full.pdf and https://news.northeastern.edu/2016/09/29/study-using-big-data-to-monitor-societal-events-shows-promise-but-the-coding-tech-needs-work — Wang et al. figures

## Caveats (verbatim)

Several fetches were summarized by a small model, not read verbatim. The rate-limit text, lastupdate.txt, GEO API, gdelt-bq, GDELT 3.0, Weller, Ward, Hammond and ICEWS end date are not found/unverified. The about.html copyright reads 2013-2022.

## Orchestrator note

The premise in my brief that POLECAT comes from the Cline Center was wrong; the agent corrected it (Program on Geostrategic Risk). The 2016 Science finding (about one in five GDELT protest events corresponded to a real protest in the test) is the single most important fact about GDELT for this project: GDELT is a signal of attention and volume, never a record of events. POLECAT's apparent staleness (last Dataverse release 2024-08-16) means it is a research corpus, not a live feed, until a newer release is confirmed. The PLOVER ontology itself (not the dataset) is a candidate for Canary's own event-type vocabulary.
