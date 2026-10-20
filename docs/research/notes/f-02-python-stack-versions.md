# F-02: Python stack: current versions, licenses, status

- Date: 2026-10-20
- Agent: researcher (Sonnet, low effort), 5 tool uses (PyPI JSON API, Hugging Face API, GitHub releases API, endoflife.date)

## Answer (verbatim; read 2026-10-20; format: name version, date, license, status)

1. Runtime/web
- Python 3.15.0, 2026-10-09, PSF, active (3.14.8 on 2026-09-30 is the prior minor)
- FastAPI 0.153.0, 2026-10-20, MIT, active
- Starlette 1.9.0, 2026-10-18, BSD-3, active
- Pydantic 2.14.1, 2026-10-11, MIT, active
- SQLAlchemy 2.1.5, 2026-10-16, MIT, active (needs Python 3.11+)
- Alembic 1.20.0, 2026-09-11, MIT, active
- uvicorn 0.54.0, 2026-09-25, BSD-3, active
- httpx 0.28.1, 2024-12-06, BSD-3, low activity (no release for 22 months)
2. Ingestion
- feedparser 6.0.14, 2026-07-30, BSD-2, active
- trafilatura 2.3.1, 2026-10-06, Apache-2.0, active
- courlan 1.4.0, 2026-06-01, Apache-2.0, active
- newspaper4k 0.9.6, 2026-07-19, MIT, active
- readability-lxml 0.9, 2026-08-27, Apache-2.0, low/moderate activity
- langdetect 1.0.9, 2021-05-07, MIT, stale
- lingua-language-detector 2.2.0, 2026-03-09, license not shown in metadata (Apache-2.0 per my recollection, unverified), active; needs Python 3.12+
- python-dateutil 2.9.0.post0, 2024-03-01, dual Apache/BSD, low activity
- dateparser 1.4.3, 2026-09-03, BSD-3, active
3. NLP
- spaCy 3.8.16, 2026-08-24, MIT, active
- xx_ent_wiki_sm 3.8.0, 2024-09-30, license not checked, available but unchanged for two years
- spacy-transformers 1.4.0, 2026-03-17, MIT, maintained
- GLiNER 0.2.29, 2026-09-08, Apache-2.0, active
- sentence-transformers 6.1.0, 2026-09-18, Apache-2.0, active
- BAAI/bge-m3, MIT, last modified 2024-07-03
- intfloat/multilingual-e5-large, MIT, last modified 2026-04-02
- datasketch 2.0.0, 2026-07-05, MIT, active
- simhash 2.1.2, 2022-03-03, MIT, stale
4. Statistics
- ruptures 1.1.10, 2025-09-10, BSD-2, low activity; Python <3.14 only, so it will not install on 3.14 or 3.15
- statsmodels 0.15.0, 2026-08-27, BSD-3, active
- scipy 1.18.1, 2026-08-21, BSD-3 (metadata field is garbled), active
- PyMC 6.3.2, 2026-09-08, Apache-2.0, active
- scikit-learn 1.9.1, 2026-09-10, BSD-3, active
- Farrington port: not searched, so not found
5. Geo
- geopandas 1.2.0, 2026-09-28, BSD-3, active
- shapely 2.2.0, 2026-10-07, BSD-3, active
- pyproj 3.8.0, 2026-09-05, MIT, active
- reverse_geocoder 1.5.1, 2016-09-15, LGPL, abandoned
- geocoder 1.38.1, 2018-04-04, MIT, abandoned (and it wraps online APIs, not a GeoNames gazetteer)
- mordecai3 3.5.0, 2026-10-06, MIT, active on PyPI
6. LLM
- anthropic 1.15.0, 2026-10-15, MIT, active
- instructor 1.17.0, 2026-09-09, MIT, active
7. Jobs
- Procrastinate 3.10.0, 2026-09-23, license field empty (MIT classifier is present), active
- APScheduler 3.11.3, 2026-06-28, MIT, active. Latest 4.x on PyPI is 4.0.0a6 (2025-04-27), alpha only, so 3.x is the stable line.

## Evidence

- https://pypi.org/pypi/<name>/json — queried for every PyPI item above (version, upload date, license, requires_python)
- https://huggingface.co/api/models/BAAI/bge-m3 and .../intfloat/multilingual-e5-large — license and lastModified
- https://api.github.com/repos/explosion/spacy-models/releases — xx_ent_wiki_sm 3.8.0 and 3.7.0
- https://endoflife.date/api/python.json — Python 3.15.0 and 3.14.8 release dates

## Caveats (verbatim)

"Active" is judged from release recency only. I did not read GitHub issues or commit history. Python 3.15.0 is only 11 days old, and ruptures, lingua and others may not yet support it. The Python.org page fetch returned nothing, so endoflife.date was used instead. Lingua's and pymc's license fields were blank or free-text on PyPI.

## Orchestrator note

Two practical consequences: pin the runtime to Python 3.13 for the first phase (ruptures excludes 3.14+, and a two-week-old 3.15 is not a base for a long-lived service), and treat the change-point library as replaceable (ruptures is low-activity; PELT and binary segmentation are small enough to vendor if it goes unmaintained). mordecai3 being active matters: it is the one maintained toponym-resolution library against GeoNames.
