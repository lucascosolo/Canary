# H-05: Access re-check of Phase 0 sources, correcting earlier notes

Read 2026-11-04 by the orchestrating session, in the local browser and with direct requests.

- **V-Dem Country-Year: A-01 is out of date.** A-01 called the download form-free. The page
  https://v-dem.net/data/the-v-dem-dataset/country-year-v-dem-fullothers-v16/ now presents a form with
  Email, Gender and a privacy approval before the CSV. V-Dem also says: "For R users, we recommend to
  install our vdemdata R package which includes the most recent V-Dem dataset". The repository
  https://github.com/vdeminstitute/vdemdata holds `data/vdem.RData` (33,878,255 bytes, gzip) with no form.
  Its DESCRIPTION says Version 16.0 and License GPL-3.
- **V-Dem ERT: the terms are now found, H-03 and H-04 are superseded.** The data page is
  https://v-dem.net/data/ert-dataset/, which links its CSV to https://github.com/vdeminstitute/ERT/tree/master/inst.
  That repository holds `inst/ert.csv` and `data/episodes.rda`, and its DESCRIPTION says Version 16.0 and
  License GPL-3. The author's reading: the package licence covers the files it ships, which permits
  storing and showing them. The page itself states no separate data licence.
- **UCDP Candidate: the registry URL went stale within weeks.** https://ucdp.uu.se/downloads/ now lists
  `GEDEvent_v26_0_9.csv` and `GEDEvent_v26_01_26_09.csv`, so an adapter must discover the file from the page.
- **Cline Center: scripted requests are refused.** A plain request to
  https://databank.illinois.edu/datasets/IDB-7095878 returned HTTP 403 while the page renders in a browser.
  Canary does not disguise its client, so this source needs a file the user downloads by hand.
  The registry endpoint from D-03 pointed at an older record, IDB-8026876 (v2.1.3).
- **Open without a key on this date:** World Bank Indicators API, the Early Warning Project CSV,
  Our World in Data chart CSVs, GeoNames `countryInfo.txt`, Natural Earth from naciscdn.org.
