# USER-01: US federal open-data portals (user suggestion, 2026-10-20)

- Date: 2026-10-20
- Source: pasted by the user mid-session with the comment "just some suggestions, take them with a grain of salt". Not verified by this session; recorded as leads.

## Pasted content (verbatim)

Start here

    Data.gov — statutory federal open-data catalog (OPEN Government Data Act). Search catalog.data.gov.
    Data.gov APIs — catalog metadata; register a free key. Does not serve the underlying files.
    api.data.gov — General Services Administration (GSA) gateway used by many agency APIs.
    resources.data.gov — federal open-data guidance.
    GeoPlatform.gov — geospatial datasets (Federal Geographic Data Committee); harvests geospatial records from Data.gov.

Agency portals found in official sources

These are examples of public, machine-readable platforms. This is not a complete list.

    Census Bureau open data
    Treasury Fiscal Data (downloads and APIs; reuse allowed for commercial and non-commercial use per that site)
    Department of Labor Open Data Portal
    Department of Education Open Data Platform
    Social Security Administration Open Data
    GSA Open Technology data
    NASA Open Data Portal
    HHS open data — including HealthData.gov, Centers for Medicare & Medicaid Services (CMS) data, data.cdc.gov, Health Resources and Services Administration (HRSA), Substance Abuse and Mental Health Services Administration (SAMHSA)
    EPA geospatial / open data

For a news dashboard, use catalog.data.gov (and its Catalog API) as the discovery layer, then pull files or APIs from the publishing agency listed on each record. I cannot verify every agency subdomain that publishes data.

## Orchestrator note

These are United States official sources. START.md insists the project is global, so they are evaluated as the US instance of a general pattern: each country's national open-data catalog (CKAN or similar) is a discovery layer, and the publishing agency is the source of record. The pattern is adopted in the source-registry design (`docs/03`): a "catalog" source type that lists datasets, and "dataset" sources harvested from it. The US portals most relevant to Canary's domains are Treasury Fiscal Data (public debt, spending), Census (population) and labour statistics; health and NASA portals are out of scope for the first release. None is verified in this session; they enter the catalog with status "lead".
