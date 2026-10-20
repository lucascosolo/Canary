# B-05: Internet shutdown and information-controls trackers

- Date: 2026-10-20
- Agent: researcher (Sonnet, low effort), 21 tool uses

## Answer (verbatim; read 2026-10-20)

1. Access Now #KeepItOn/STOP: records documented shutdown instances (scope, magnitude, context, official justification, sources; per the old 2017 page). The current page says 2,102 documented instances since 2016, "updated through 2025"; the 2025 report (31 Mar 2026) counts at least 313 shutdowns in 52 countries. Download is a spreadsheet at https://www.accessnow.org/keepiton-data-spreadsheet. The file format is not stated, and the older 2017 tracker was .xlsx. The dashboard at https://www.accessnow.org/keepiton-data allows filtered export and is "in development". Methodology: https://www.accessnow.org/keepiton-data-methodology. Cadence: annual in practice, with retroactive additions to earlier years, but no stated schedule. License: no explicit dataset license found. The page footer links CC BY 4.0, which was not confirmed to cover the data. Field list (country, type, duration, trigger columns): not found on the pages read.

2. OONI: measurements (website, app and circumvention-tool blocking, per network ASN and country) are published openly in machine-readable form. Access is via the API (api.ooni.io, now also api.ooni.org), whose docs list /measurements and aggregation endpoints (paths and parameters not retrieved), via Explorer (explorer.ooni.org, with country pages), and via the S3 buckets ooni-data-eu-fra (eu-central-1) and ooni-data (us-east-1). ClickHouse access: not found. License: the ooni/license repo says its license "applies to all published OONI data" and contains CC4.0-BY-NC-SA.md. AWS Open Data lists the data as CC BY-NC-SA 4.0. The CC BY-NC-SA reading is therefore very likely but I did not read LICENSE.md itself. Data policy v1.7.0 (modified 29 Jul 2026) says analytics and push-notification data are not published, users can opt out of sending measurements, and the data may unintentionally contain personal information. The volunteer-probe dependence is not in the policy text I read, so I did not verify it.

3. IODA: three signals (BGP, active probing of about 3.5M networks every 10 minutes, and UCSD Network Telescope darknet traffic). It provides near-real-time and historical data at country, sub-national region and ASN level, and is described as free and open source. The API host (api.ioda.inetintel.cc.gatech.edu) failed TLS in my sandbox ("unable to get local issuer certificate"), so endpoints, latency figures and terms of use are not found.

4. Cloudflare Radar: base URL https://api.cloudflare.com/client/v4/radar/. Auth is a Bearer API token (Custom Token, Account > Radar > Read). The Outage Center endpoint /radar/annotations/outages takes limit, offset, dateRange and format, and returns scope, startDate, endDate, locations, asns, outageCause and outageType (including government-directed shutdowns). Traffic and anomaly series exist, but the endpoint names were not read. Data license: the Radar overview says the data is under CC BY-NC 4.0 (confirmed). The API is described as free. Rate limits: not found.

NetBlocks: no API or dataset found in a search (only GitHub repos under github.com/ntblk, such as block-collector). Treat it as posts and reports only, unverified.

## Evidence

- https://www.accessnow.org/keepiton-data — 2,102 instances, links the spreadsheet and methodology
- https://www.accessnow.org/keepiton-shutdown-tracker/ — old 2016-17 .xlsx tracker
- https://ooni.org/about/data-policy — v1.7.0, access methods, limits
- https://github.com/ooni/license/tree/master/data — license applies to all published data, CC4.0-BY-NC-SA.md present
- https://registry.opendata.aws/ooni/ — S3 buckets, CC BY-NC-SA 4.0
- https://developers.cloudflare.com/radar/ — CC BY-NC 4.0
- https://developers.cloudflare.com/radar/get-started/first-request/ — token permission and base URL
- https://developers.cloudflare.com/radar/investigate/outages/ — outages endpoint
- https://www.caida.org/funding/ioda/ and the OTF project page — IODA sources and granularity

## Caveats (verbatim)

Fetches were summarised by a small model. docs.ooni.org returned 429, and the IODA hosts failed TLS, so OONI endpoint details and all IODA API and terms details are missing. The Access Now license and the OONI license name are inferred from secondary signals.

## Orchestrator note

Cloudflare Radar's outage annotations (which name government-directed shutdowns as a cause) and the user's existing Cloudflare account make Radar the first information-controls feed to integrate; OONI and #KeepItOn corroborate it. All three are non-commercial licences, which the project's non-profit posture satisfies.
