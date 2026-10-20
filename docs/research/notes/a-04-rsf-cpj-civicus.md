# A-04: RSF World Press Freedom Index, CPJ databases, CIVICUS Monitor

- Date: 2026-10-20
- Agent: researcher (Sonnet, low effort), 12 tool uses

## Answer (verbatim)

1. RSF Index: The CSV is linked from the index page as "Download this index" at https://rsf.org/sites/default/files/import_classement/2026.csv. The year switcher covers 2002-2026 (2011 and 2012 are combined). I saw no XLSX link. The five indicators are political, economic, legal, sociocultural and security, plus a global score. Cadence is annual. The 2026 edition is probably April 2026, but that is inferred only from a PDF upload path of /2026/04. I found no RSF license or reuse text on the page. The R package pressfreedom.data says reuse is unrestricted, but that is a third-party claim, not RSF's. Media Ownership Monitor (mom-rsf.org country sites): I found no structured data download, only a full-site PDF per country (the Turkey FAQ says it is regenerated daily). Site content is reported as CC BY-NC-ND 4.0, from the Turkey and Mongolia FAQs via search snippet. EurOMo, a related project, offers BODS v0.3 downloads.

2. CPJ: Three databases (killed, imprisoned, missing) cover 1992 onward. Imprisoned includes an annual 1 December snapshot, and "currently imprisoned" is a live view. CPJ says the data is "updated continually". A beta REST API exists (GET /v1/persons/{id}, with filtering, sorting, pagination and aggregations), but its page says "As of April 23, 2024, access is temporarily unavailable". I found no CSV export. The API page says text is CC BY-NC-ND 4.0, which means no derivatives and non-commercial use, and I did not find a separate data-specific license. CPJ launched a new data management system in 2025. In June 2026 it removed 8 names from the killed database after a review, and a September 2026 audit recommended publishing all 22 removed names. Records are therefore revised, so snapshot and date your pulls.

3. CIVICUS Monitor: Five ratings by score out of 100: Closed (1-20), Repressed (21-40), Obstructed (41-60), Narrowed (61-80), Open (81-100). The country table has about 199 entries, including some unrated territories (Greenland is "under review"). The data page offers ratings for 2018-2024 plus current, a year selector, embeddable maps and a data download. The page showed "Data last updated Dec 2025", which suggests an annual ratings update in December. The Watchlist was last updated 29 July 2026 (Bahrain, Burkina Faso, Ecuador, Georgia, India); it appears to be issued a few times a year, but I did not confirm the cadence. Site footer license: CC BY-SA 4.0. RSS for country updates and incidents: not found. Machine-readable access to the underlying civic-space updates: not found.

## Evidence (read 2026-10-20)

- https://rsf.org/en/index — CSV link, years 2002-2026, five indicators; no license text.
- https://cpj.org/data/ — three datasets since 1992, "updated continually"; no export or terms.
- https://cpj.org/data-api/ — beta API, access unavailable since April 2024, CC BY-NC-ND 4.0.
- https://monitor.civicus.org/ — rating bands, about 199 entries, "Data last updated Dec 2025", Watchlist 29.07.2026, CC BY-SA 4.0.
- https://monitor.civicus.org/data/ — 2018-2024 ratings plus current, download offered.
- https://monitor.civicus.org/about/ — CC BY-SA 4.0 footer.
- Web search results, not read directly — CPJ June and September 2026 removals; MOM FAQs at turkey.mom-rsf.org/en/about/faq/ and mongolia.mom-rsf.org/en/about/faq/.

## Caveats (verbatim)

The fetch tool summarizes pages and does not return raw text, so these are summaries. I did not download any file, so CSV columns and formats are unverified. The RSF terms page, CPJ methodology and FAQ pages, and CIVICUS ratings page returned 404 at the guessed URLs. The CIVICUS download format was not confirmed. Watchlist cadence is not stated on any page I read. A CC BY-SA license on the CIVICUS site may not cover the underlying data. Check the actual license pages before redistributing any of it.

## Orchestrator note

The CPJ record revisions of 2026 are a concrete example of why the system must snapshot upstream datasets by retrieval date and treat "source corrected its record" as a distinct event from "we corrected our processing" (START.md section 11).
