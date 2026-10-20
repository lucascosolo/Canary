# 02. Research and competitive landscape

Everything in this document was researched on 2026-10-20 by researcher agents reading primary
pages; each paragraph names the note in `research/notes/` that holds the URLs, the date read and
the agent's own caveats. Where the agent could only reach a search snippet or an abstract, the
note says so and this document repeats the caveat. The sandbox proxy blocked some hosts outright
(eiu.com, ipcinfo.org, crisisgroup.org, un.org document pages, acaps.org API pages, several
publisher sites); those entries are marked "to re-read in a browser" and are listed again in
document 12.

## 1. What already exists

### 1.1 Annual and periodic indices of democracy, rights and governance

These describe level, not change within a year, and they are the backbone of the baseline layer
(document 04).

V-Dem is the richest and the most openly licensed: version 16 (March 2026), 202 country units,
some series back to 1789, 531 indicators and 251 indices, CC BY-SA 4.0 with commercial use
allowed, annual every March, downloadable without registration, no API (note A-01). Its Episodes
of Regime Transformation dataset (ERT 16.0) codes autocratization and democratization episodes
with start and end years and is the natural episode list for the historical library (A-01, G-04).
Its V-Party dataset carries the anti-pluralism index (`v2xpa_antiplural`) that operationalises
"parties that propose restricting liberties", although version 2 ends in 2019 and its licence
was not confirmed (E-02). Its media variables (`v2mecenefm`, `v2meharjrn`, `v2mebias`) are confirmed
in the v16 codebook (G-01).

Freedom House (Freedom in the World 2026, 195 countries and 13 territories; Freedom on the Net
2025, 72 countries; Nations in Transit 2024, 29 countries) is free for personal, academic and
non-profit use with citation, needs prior approval for commercial use, is distributed as
spreadsheets, sometimes by request, and has no API (A-02). International IDEA's Global State of
Democracy indices (174 countries, 30 indices, annual, about half built on V-Dem) are downloadable,
with licence and format not confirmed (A-02). The EIU Democracy Index could not be verified at all
because eiu.com is blocked from here; treat its scores as needing written permission (A-03).
Polity5 ends in 2018, PITF stopped supporting it in 2020, and CSP requires written permission to
reproduce it; it is a backtesting input only (A-03). BTI (137 developing and transition countries,
biennial, free spreadsheets, licence unstated) is a useful cross-check (A-03).

Press freedom and civic space: RSF's index is a CSV covering 2002 to 2026 with no stated licence
(A-04); CPJ's databases of killed, imprisoned and missing journalists are continuously updated,
revised after the fact (eight names removed in June 2026), licensed CC BY-NC-ND for text, and the
beta API has been offline since April 2024 (A-04); the CIVICUS Monitor rates about 199 countries
on a five-band civic-space scale, updates ratings annually in December and a watchlist a few
times a year, and carries a CC BY-SA 4.0 site licence whose application to the data is
unconfirmed (A-04). Transparency International's CPI is CC BY-ND (no derivatives) and comparable
only from 2012 (A-05). The Political Terror Scale (updated September 2026), CIRIGHTS, HRMI
(CC BY-NC) and the Academic Freedom Index are annual rights indices with stated or inferable
terms (E-03). The World Bank's Worldwide Governance Indicators were recalculated back to 1996 in
the 2025 edition and carry a usage advisory rather than a licence (C-01).

### 1.2 Event and conflict data

UCDP is the cleanest conflict-event source: all datasets CC BY 4.0, bulk CSV without a token,
monthly "Candidate" events lagging a month at most, the annual GED (v26.1, 1989-2025), and a
free API with a token obtainable by email and a 5,000 requests-a-day quota (B-02). Its 25-death
threshold and media dependence are known limits.

ACLED's position changed in 2024-2025: access is through a myACLED account with four tiers set
by the organisation, the EULA licenses non-commercial use only, says a licensee's "own dashboard"
is not a permitted use, bars giving others direct access to the content, and the content-usage
terms restrict AI and machine-learning use regardless of purpose (B-01). ACLED's own codebook
states that fatality data are "typically the most biased and least accurate component of conflict
reporting". The published UCDP-ACLED comparisons (Eck 2012; Öberg and Yilmaz 2025 versus Raleigh,
Kishi and Linke) disagree about why the two datasets diverge (B-01, B-02). Until ACLED's Access
team answers in writing, ACLED is a link, not a feed.

GDELT is free for any use with attribution, updates every fifteen minutes, machine-translates 65
languages, and provides URLs and extracted fields rather than article text (B-03). The decisive
fact about it is the 2016 Science evaluation in which only about a fifth of GDELT-reported
protests in a Latin American test corresponded to real protests and duplication from re-reporting
was pervasive (Wang et al. 2016, via secondary summaries; B-03). GDELT is therefore a measure of
attention and volume, never a record of events. POLECAT, the ICEWS successor coded with the
PLOVER ontology, is CC0 but its last Harvard Dataverse release is dated 2024-08-16 (B-03); the
ontology is reusable, the dataset is not a live feed until a newer release appears.

Coups: the Cline Center dataset (v2.2.2, February 2026, 1,161 events from 1945, CC BY) is a
usable, current outcome series (D-03). Powell and Thyne's dataset could not be reached.

### 1.3 News and the information ecosystem

No affordable commercial news API returns full text with redistribution rights: NewsAPI's free
tier is development-only and its business tier costs $449 a month without full text; GNews's
cheapest paid tier is about EUR 50 a month with full content but non-commercial free use only
(B-04). Media Cloud is active (commits through October 2026, over a billion stories from over
25,000 sources), offers story search by national media collection through an API key, publishes
its fetcher and indexer code under Apache 2.0, and does not appear to return full text (B-04,
F-06). Common Crawl's CC-NEWS provides daily WARC files from 2016 but its terms place copyright
risk on the user (B-04). Google's terms prohibit automated access that violates robots.txt (B-04).

Information controls: Cloudflare Radar's outage annotations (which name government-directed
shutdowns as a cause), OONI's measurements and the Access Now #KeepItOn dataset are all
machine-readable and all carry non-commercial or share-alike licences (B-05). IODA could not be
reached. NetBlocks publishes no data.

Source reliability: NewsGuard is commercial and single-score, Media Bias/Fact Check is rejected
by a 2026 preprint for research use, the Journalism Trust Initiative has no machine-readable
registry, and the Global Disinformation Index rates domains by risk (G-01). Syndication
detection has textbook answers (shingling and MinHash; Churnalism-style press-release overlap)
and the wire share of news is large (Pew 2015: about six in ten national-government stories in
eight US papers were wire copy) (G-01). The State Media Monitor's matrix of 546 state-administered
outlets in 151 countries and the RSF/GMR Media Ownership Monitor (27 countries) are the ownership
references (G-01).

### 1.4 Humanitarian, economic and displacement data

ReliefWeb's API is free with a pre-approved app name since November 2025 and 1,000 calls a day,
with content generally CC BY 4.0 but partner reports under their own copyright (B-06). HDX's HAPI
needs only an app identifier; whether ACLED-derived fields in it inherit ACLED's terms is an open
question for HDX (B-06). The World Bank Indicators API needs no key and most datasets are CC BY
4.0 (C-01). The IMF retired its legacy portal in November 2025 and now serves SDMX 2.1 and 3.0;
its terms allow non-commercial reuse with attribution, which fits Canary (C-01). OECD and ILO
APIs exist with unconfirmed rate limits and licences; Our World in Data serves chart CSVs and a
Parquet catalog, CC BY 4.0 for its own series with upstream licences preserved in metadata (C-01).
UNHCR's Refugee Data Finder API needs no credentials but its licence was not readable; IOM DTM's
terms require written permission for any redistribution; IDMC, WFP and FEWS NET pages were not
readable from here (H-02). SIPRI allows citation freely but limits reproduction to under a tenth of
a dataset for non-commercial use (E-04). OpenSanctions aggregates sanctions and PEP lists under
CC BY-NC 4.0 with four daily updates and a self-hostable API (A-05, E-04).

### 1.5 Elections, legislation and law

ElectionGuide permits free non-commercial use with attribution but has no public API; IPU Parline
is open data with an API whose licence variant was not found; NELDA codes election conduct to
2020; the Manifesto Project is research-only with no redistribution; observation missions
publish PDFs (E-02). There is no global legislative feed: Congress.gov, the UK Parliament, EUR-Lex,
the Bundestag, the French Assembly and Brazil's Câmara have APIs with varying terms; India,
Hungary, Türkiye, Israel, Mexico and Indonesia were not established; the Law Library of Congress
Global Legal Monitor, ICNL's Civic Freedom Monitor (72 entries, updated in October 2026), and the
Venice Commission are curated secondary trackers (E-01). UN documents are not free to reuse by
default: the UN's terms allow personal non-commercial use only, with news material usable with
credit (E-03, E-04).

### 1.6 Monitoring platforms and early-warning systems

International IDEA's Democracy Tracker (monthly, 173 countries, methodology being adapted in
2026) and Crisis Group's CrisisWatch are the closest public analogues; neither is machine-readable
or shows per-claim evidence (A-02, F-06). The CFR Global Conflict Tracker covers 27 conflicts.
Protect Democracy's Authoritarian Threat Index and Bright Line Watch are US-only expert surveys.
Commercial platforms (Dataminr, Recorded Future, Janes, FiscalNote, Seerist, Verisk Maplecroft)
are closed (F-06). The Early Warning Project publishes an annual statistical risk assessment for
more than 160 countries with a downloadable CSV, a GitHub repository and a public accuracy page
(A-06, G-03). ViEWS publishes open monthly forecasts of state-based conflict fatalities 1 to 36
months ahead, with code on GitHub (B-02). The EU's GCRI, Germany's PREVIEW, the AU, ECOWAS and
IGAD systems, and the US Atrocity Early Warning Task Force all exist and none publishes open live
data; the published critiques concern response, not detection (F-07).

### 1.7 Open-source components worth reusing

Media Cloud's `rss-fetcher`, `feed_seeker`, `story-indexer` and `metadata-lib` (Apache 2.0);
Bellingcat's `auto-archiver` (MIT) for preserving cited pages; OpenSanctions' `yente` (MIT) for
entity screening; HURIDOCS Uwazi (MIT) as a reference for human-rights documentation workflows;
`mordecai3` (MIT, active) for toponym resolution against GeoNames; `trafilatura` for article
extraction; the Internet Archive's availability and CDX APIs for link permanence (F-02, F-06,
H-01). A GitHub search for early-warning projects for political violence active since mid-2024
returned nothing (F-06).

## 2. What the academic literature settles, and what it does not

- Backsliding is gradual and legal, mostly led by elected incumbents (33 of 47 episodes in one
  count), and the field admits it lacks diagnostic tools for gradual decline (D-01).
- Resilience is real and measurable: of 84 completed autocratization episodes in democracies
  since 1900, 23% averted breakdown; judicial constraints and a country's democratic stock help at
  both the onset and the breakdown stage; coups hurt at both (Boese et al. 2021, read in full,
  D-01). V-Dem's 2025 brief puts U-turns at 46% of episodes starting in democracies, a figure that
  circulates in two versions and must be checked against the primary text (D-01).
- Erosion halts when institutional constraints meet a trigger such as a downturn or scandal, and
  all three accountability channels (horizontal, diagonal, vertical) feature in the halted cases
  (Laebens and Lührmann 2021, abstract-level, D-01).
- No theory predicts backsliding well; the review literature calls explanations "inchoate"
  (Waldner and Lust 2018, D-01). That is the strongest argument for an indicator-and-evidence
  system rather than a predictive model.
- Structural atrocity and instability models (Harff 2003, Goldstone et al. 2010, EWP) reach
  70-80% headline accuracy by ranking slow structural risk two years ahead against a base rate of
  one or two onsets a year; EWP's own accuracy page reports about 64% of onsets in its top 30 two
  years ahead and about 20 false positives per onset at a 4% threshold (D-02, G-03).
- Conflict onset in previously peaceful countries is the "hard problem"; news-text models help
  most exactly there, and the theory-versus-machine-learning dispute (Blair and Sambanis versus
  Beger, Morgan and Ward) is unresolved (D-03). The 2024 ViEWS challenge scores distributional
  forecasts with CRPS (D-03).
- Coup forecasts can have good ranking (AUC-ROC about 0.8) and still be wrong almost every time
  they flag a country (AUC-PR 0.02 to 0.05) because fewer than 4% of country-years have an attempt
  (D-03). Any rare-event warning must be evaluated with precision-recall and false-alarm ratio
  against base rate, never with accuracy (G-03).
- From other fields: the signals approach picks indicator thresholds by historical noise-to-signal
  ratio within a declared 24-month window (C-02); public-health surveillance models an expected
  count and flags exceedances, with staff curating every classified report daily (HealthMap, C-02);
  the IPCC separates the amount of evidence from the agreement among sources and derives confidence
  from both, and ICD 203 forbids putting a likelihood word and a confidence level in one sentence
  (C-03); the Admiralty system grades source reliability and information credibility on two
  separate axes (C-03); Neustadt and May's procedure for analogies (likenesses, differences,
  unclear; placement; time-lines) and Khong's warning that analogies get chosen by salience are
  the method for historical comparison (G-04).
- LLM extraction is a measurement instrument that must be validated per task and per model
  version: codebook-following can stay near 0.20 weighted F1 while headline scores rise; citation
  support fails half the time on open-ended tasks without checking; untrusted document text must
  never influence control flow (F-05).

## 3. Where Canary adds something

The research found no open system that (a) spans institutions, rights, conflict, information
and economy for every country, (b) separates level from change from assessment, (c) shows per-claim
evidence with source independence accounting, (d) tracks improvement and resilience on equal terms,
(e) makes coverage gaps visible, (f) documents its historical comparisons with a stated procedure,
and (g) publishes its own misses and false alarms. Each of those is individually practised
somewhere (IPCC confidence language, HealthMap's curation, EWP's accuracy page, Neustadt and
May's procedure, UCDP's transparency); none is combined in a public monitor. That combination,
not a new forecasting model, is the product.

## 4. What the research could not establish

A running list, carried into document 12 as first actions for the next session with a browser:
EIU terms; IPC Technical Manual 3.1 (evidence levels, confidence stars); CrisisWatch structure and
terms; UN Digital Library OAI-PMH; ACAPS licence; INFORM licence and cadence; IDMC, WFP and FEWS
NET access; ACLED's tier limits and a written answer on dashboards; HDX's position on ACLED-derived
fields; IPU Parline licence and API; Constitute licence; Freedom House data-request flow; RSF
licence; CIVICUS data licence; OONI endpoint details; IODA API; Metaculus terms; the V-Dem U-turn
figures; the Admiralty doctrine text; ERT codebook variables; GTD current regime; WJP licence;
psdata.un.org contents.
