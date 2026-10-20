# B-06: ReliefWeb API, HDX and HAPI, ACAPS, INFORM Risk

- Date: 2026-10-20
- Agent: researcher (Sonnet, low effort), 17 tool uses

## Answer (verbatim; read 2026-10-20)

1. ReliefWeb API: free, read-only, all site content (reports, disasters, jobs, training, countries, sources) via API with filters. Every request needs an appname; since 1 Nov 2025 it must be a pre-approved appname (the old self-chosen appname no longer works). Limits: max 1000 entries per call, 1000 calls per day; higher needs reviewed case by case. Calls may be logged. Licence: ReliefWeb site content is generally CC BY 4.0 with noted exceptions, but partner-contributed reports, jobs and training may be copyrighted by the publishing organisations, so you must respect source IP. Whether report body/summary fields are returned: not confirmed on the page I read (it only says all content is available); the response structure is on a separate Results page I did not read.

2. HDX/HAPI: HAPI needs an app_identifier query parameter, generated via the sandbox encode_identifier endpoint (application name plus email); no approval is described. Terms: max 10,000 entries per call, a request to keep to 1 request per second, usage logged. Confirmed endpoints: coordination-context/operational-presence, population-social/population, metadata/*. HAPI's stated aim is to cover all HDX data-grid subcategories; I could not read the list, so food security/IPC, conflict events, humanitarian needs, funding and refugees are not confirmed here. A HAPI licence and the ACLED position were not found: the HAPI terms page I read has no licence, attribution or ACLED section, so whether ACLED-derived data in HAPI is bound by ACLED's own terms is not found. ACLED's own terms (via search snippet) prohibit giving others direct access to its raw data, which makes this an open risk to check with hdx@un.org. The HDX CKAN API and per-dataset licences: not found (data.humdata.org returned 403).

3. ACAPS: api.acaps.org is a Django REST API with registration at /register/ and docs at /api/v1/ (a 2021 announcement describes a token from /api/v1/get-auth-token/). Datasets listed on acaps.org/en/data: INFORM Severity Index, Humanitarian Access, Protection risks monitoring, Information landscape, Seasonal events calendar, and Afghanistan, Yemen and Ukraine core datasets. Licence: not found. The pages say only "All our datasets are freely available" and link to Terms of service and Copyright pages I did not read, so CC BY is unverified. Update cadence: not found. A Severity methodology update dated 2026-02-02 exists. The "Protection Indicators" dataset name and the risk list were not confirmed.

4. INFORM Risk: described as a global open-source risk assessment for crises and disasters. The page I read did not describe the hazard and exposure, vulnerability, and lack of coping capacity dimensions; that is from prior knowledge. Latest release is "Mid 2026" (file v073), downloadable as XLSX; methodology PDF dated 2017. No API mentioned, and no licence or cadence stated.

## Evidence

- https://apidoc.reliefweb.int/ : pre-approved appname from 2025-11-01; 1000 calls/day, 1000 entries; CC BY 4.0 with partner-copyright caveat
- https://hdx-hapi.readthedocs.io/en/latest/getting-started/ : app_identifier via encode_identifier
- https://docs.humdata.org/about/hdx-terms-of-service/hapi-terms-of-service : 10,000 entries cap, 1 req/s, logging
- https://hdx-hapi.readthedocs.io/en/latest/ : use governed by HAPI Terms of Use
- https://www.acaps.org/en/data : dataset list, "freely available", register link
- https://api.acaps.org/ and https://api.acaps.org/practical-guide/ : login/register, /api/v1/ docs
- https://drmkc.jrc.ec.europa.eu/inform-index/ : Mid 2026 XLSX, no API or licence stated
- https://acleddata.com/faq/how-can-i-access-and-use-acled-data : ACLED redistribution restriction (search snippet only)

## Caveats (verbatim)

Several pages returned 403 or 404 (hapi.humdata.org/docs, data.humdata.org terms and /hapi, acaps.org API pages). Fetch summaries came from a small model, not verbatim. ACLED, ACAPS licence, INFORM licence and cadence, and HAPI theme list remain unverified. Direct reads of the ReliefWeb Results page, ACAPS Terms of service, JRC INFORM licence and the HDX docs index (docs.humdata.org/llms.txt) would close most of these gaps.

## Orchestrator note

ReliefWeb's 2025 move to pre-approved app names is a small example of an access regime changing under a project; the source registry must record the access regime and the date it was verified. The ACLED-via-HAPI question is to be put to HDX in writing before any ACLED-derived field is stored.
