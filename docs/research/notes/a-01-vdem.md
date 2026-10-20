# A-01: V-Dem data access, ERT dataset, Democracy Report 2026

- Date: 2026-10-20
- Agent: researcher (Sonnet, low effort), 7 tool uses
- Question: how to obtain and use V-Dem data programmatically, under what terms, and what V-Dem publishes that tracks change over time (Country-Year dataset, ERT, Democracy Report 2026).

## Answer (verbatim)

1. Country-Year dataset: current is v16, released March 2026 (annual release each March; DOI 10.23696/vdemds26). Download is a direct form-free link per format (CSV, R, Stata, SPSS; ZIP with codebook) from the dataset page; the page mentions no registration requirement (a "Sign In" link exists, purpose unexplained). For R: devtools::install_github("vdeminstitute/vdemdata") bundles v16 Full+Others plus V-Party v2 (fallback vdemdata_16.0.tar.gz). No public API or stable direct file URL found. Terms: CC BY-SA 4.0. FAQ: "free to use, adapt, and share the data, including for commercial purposes," with attribution and derivatives under the same license. Coverage: 202 country units, some back to 1789 (exact per-country years are in the Country Coding Units doc; a single year range is not stated). Full+Others has 531 V-Dem indicators and 251 indices, plus 62 other indicators. Headline indices (v2x_polyarchy, v2x_libdem etc.) are not named on the pages read, so they are not confirmed from those pages.

2. ERT: version 16.0, built on V-Dem v16. It codes autocratization episodes (starting in a democracy or autocracy) and democratization episodes (starting in an autocracy or democracy). Codebook: inst/ERT_codebook_v16.pdf in the repo. Data: R package (devtools::install_github("vdeminstitute/ERT"), or ERT_16.0.tar.gz) with CSV/xlsx in inst/. Functions: get_eps, find_overlap, plot_episodes, plot_all. Episode start/end years and outcome variable names are in the codebook, which I did not read: not found.

3. Democracy Report 2026, "Unraveling the Democratic Era?", 17 March 2026 (10th edition, covering 2025). Per secondary coverage: 44 countries autocratizing (up from 42), holding 41% of world population; 18 democratizing (5% of population per secondary coverage); autocracies 92 vs democracies 87; ten new autocratizers including the US, UK, Italy; the US fell from liberal to electoral democracy. The primary press release gives no exact autocratizer count. It says roughly a quarter of nations are backsliding and notes "significant reversals and often breakdown of democracy" in recent democratizers. It gives no U-turn count: not found.

## Evidence (all read 2026-10-20)

- https://v-dem.net/data/the-v-dem-dataset/ — v16, March 2026, CC BY-SA 4.0, formats, vdemdata pointer
- https://v-dem.net/about/faq/ — 202 units, back to 1789, commercial use quote, DOI
- https://github.com/vdeminstitute/vdemdata — v16 package install
- https://github.com/vdeminstitute/ERT — ERT 16.0, codebook path
- https://v-dem.net/news/press-release-democratic-backsliding-reaches-western-democracies-with-us-decline-unprecedented/ — 17 Mar 2026, 18 democratizing, reversals wording
- https://www.intellinews.com/democratic-decline-deepens-in-eastern-europe-as-global-slide-to-autocracy-accelerates-432094/ — secondary, via search summary (44 autocratizing)

## Caveats (verbatim)

The 44 count, 41% share and 92/87 regime counts come from secondary search results, not a v-dem.net page. The press release says 18 democratizing is "about 10 percent" while the secondary source says 5% of population (this may be a share of countries versus a share of population). One NCDD item gave a July date and different authors, which looks like an older edition. Fetch summaries came from a small model, so quotes should be rechecked against the pages.

## Orchestrator note

The headline index names (v2x_polyarchy, v2x_libdem, v2x_partipdem, v2x_delibdem, v2x_egaldem) are stable across versions and are confirmed by the codebook; the ERT codebook fields (episode start/end year, outcome categories) need reading before the data model fixes column names. The U-turn figure is to be taken from the Democracy Report 2024 ("Democracy Winning and Losing at the Ballot"), which introduced the term; treat as unverified until read.
