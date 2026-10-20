# E-01: Legislative and legal-development data sources

- Date: 2026-10-20
- Agent: researcher (Sonnet, low effort), 30 tool uses

## Answer (verbatim; read 2026-10-20; many primary pages blocked, so several fields are "not found")

1a. IPU Parline (data.ipu.org): open data on national parliaments (about 188 parliaments, 500-600 data fields; composition, elections, women's representation, structure). It is not a legislation tracker. A 2024 redevelopment launched a Parline API and a Creative Commons licence for reuse; the licence variant is not found. Auth for the API: not found. Cadence: "updated daily" per IPU's 2024 notice. Bulk files via data.ipu.org/data-catalogue.
1b. Law Library of Congress Global Legal Monitor (loc.gov/law/foreign-news): curated articles on legal developments by country. RSS exists (2008-09 sources: topic and country feeds; the collection page points to loc.gov/subscribe/#law). Current feed URLs, API and cadence: not found. Licence: public-domain US government work is my inference; no statement read. loc.gov returned 403 to me.
1c. ICNL Civic Freedom Monitor: 72 entries (64 countries/territories plus 8 intergovernmental bodies); 57 current and 15 archived reports. Tracks association, expression and assembly. No fixed cadence stated, but reports were updated 12-19 Oct 2026. Data export: not found. Licence: not found (page shows only cookie terms).
1d. Venice Commission: opinions are pages on coe.int/en/web/venice-commission; CODICES is an open-access constitutional case-law database (about 90 courts, 10,000+ decisions). RSS, API, licence: not found.
2. Congress.gov API: key required (api.congress.gov/sign-up), 5,000 requests/hour. UK Parliament (developer.parliament.uk; Bills API, Members API): OpenAPI spec, no auth seen, © UK Parliament; OPL not confirmed. EUR-Lex: Cellar SPARQL endpoint and REST API with no registration mentioned; SOAP search web service needs registration; data dump needs an EU Login; reuse "free of charge, subject to copyright conditions". European Parliament data.europarl.europa.eu: page not extractable, so auth and licence not found. Bundestag DIP: free; every request needs an API key. A public time-limited key is posted on the help page, with no registration. A permanent personal key comes by email to parlamentsdokumentation@bundestag.de. Rate limits are unpublished. Terms are in nutzungsbedingungen_dip.pdf. France data.assemblee-nationale.fr: open data under the Etalab Open Licence (per a 2015 Assembly report), mirrored on data.gouv.fr. Brazil dadosabertos.camara.leg.br: REST API, no key mentioned, bulk CSV/XLSX/ODS/JSON/XML, licence not stated. India: no official legislative API found; data.gov.in lists bills datasets, and the Lok Sabha/Rajya Sabha sites allow non-commercial reuse with attribution. PRS Legislative Research: not found. Hungary, Türkiye, Israel, Mexico, Indonesia: not found; I did not check them.
3. Constitute (constituteproject.org): has an API and downloadable semantic-web data; the About page credits Hein and OUP texts, which may have separate terms. The CC BY-NC claim is unverified (/service/docs returned 404 or was blocked). Comparative Constitutions Project: Chronology v6.0 (through 2025), Characteristics v5.0 (Feb 2025), 18 replication datasets, all as .zip; inner formats and licence are not stated. The page says few constitutional texts are free of copyright.

## Evidence

- https://www.icnl.org/resources/civic-freedom-monitor — 72 entries, recent updates Oct 2026
- https://comparativeconstitutionsproject.org/download — versions, zip, no licence
- https://github.com/LibraryOfCongress/api.congress.gov — key, 5,000/hr
- https://dip.bundestag.de/documents/nutzungsbedingungen_dip.pdf — key policy (via search summary)
- https://eur-lex.europa.eu/content/help/data-reuse/reuse-contents-eurlex-details.html — SPARQL, registration, reuse (via search summary)
- https://dadosabertos.camara.leg.br/swagger/api.html — formats, no key mentioned
- https://developer.parliament.uk/ — API directory
- https://bills-api.parliament.uk/index.html — © UK Parliament, OpenAPI
- https://data.ipu.org/about and https://www.ipu.org/news/voices-and-videos/2026-06/ipu-parline-turns-30 — via search snippets only
- https://constituteproject.org/content/about — via search snippets only

## Caveats (verbatim)

data.ipu.org, loc.gov, constituteproject.org and venice.coe.int could not be fetched (403 or sandbox network denial). Their entries rest on search snippets and are not verified against the live pages. The Etalab, Bundestag and EUR-Lex details also come from search summaries. The OPL for the UK, the Brazil licence, the Constitute licence and the CCP licence are unconfirmed. Re-check them with a direct browser.

## Orchestrator note

There is no global legislative feed. Worldwide legislative tracking in a first release is not feasible from APIs; it has to come from curated secondary trackers (Law Library of Congress Global Legal Monitor, ICNL, International IDEA's Democracy Tracker, Venice Commission opinions) plus news-derived claims, with per-country official APIs added one at a time where they exist. The policy-lifecycle model in START.md section 3C (proposed, passed one chamber, enacted, blocked, in force, enforced) is still right; the data to fill it will be sparse and uneven, and the UI must show that.
