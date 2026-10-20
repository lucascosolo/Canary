# F-01: PostgreSQL as the single store: FTS, vectors, geo, time series, queues, graph

- Date: 2026-10-20
- Agent: researcher (Sonnet, low effort), 24 tool uses

## Answer (verbatim; read 2026-10-20)

1. PostgreSQL 18 was first released 2025-09-25, and its current minor is 18.6. The support window is 5 years per major: 18 to 2030-11-14, 17 (17.11) to 2029-11-08, 16 to 2028-11-09, 15 to 2027-11-11, 14 to 2026-11-12. PG13 is EOL. I did not verify the 17/18 feature list (async I/O in 18, incremental backup in 17) in this session: not found.
2. Built-in FTS: the tsvector limits are documented. A lexeme is under 2 kB, a tsvector under 1 MB, positions are at most 16,383, and there are at most 256 positions per lexeme. Per-language dictionaries and stemmers are fixed at index time by the text search configuration. The limits page does not mention BM25, and I did not confirm the "no native BM25" point in the ranking docs. ParadeDB pg_search is at v0.26.2 (released 16 Oct 2026). The Community edition is AGPL-3.0, and Enterprise is commercial. The docs index lists tokenizers for ICU, Lindera (CJK), Jieba, chinese_compatible and ngram, plus language stemming and stopword filters, but I did not read those pages. Assets exist for PG15, 16 and 18, and the full list of supported PG versions is not found. No source I read gives a point at which to move to OpenSearch/Elasticsearch: not found.
3. pgvector is v0.8.7. HNSW and IVFFlat are supported. `vector` can be indexed up to 2,000 dimensions and `halfvec` up to 4,000. `bit` can be indexed up to 64,000 and `sparsevec` up to 1,000 non-zero elements. Types themselves hold up to 16,000. The README says to scale vertically first, use halfvec or binary quantization, and then use replicas or sharding such as Citus. A non-partitioned table is limited to 32 TB. There is no published "N million vectors per node" figure: not found. pgvectorscale is under the PostgreSQL license, and it requires pgvector (CREATE EXTENSION ... CASCADE). Its latest release and supported PG versions are not found; the README's build example uses `--pg18`.
4. PostGIS: the current release listed is 3.6.4 (date not found; supported PG versions not found). I did not read the PostGIS docs on point-in-polygon, distance and boundary joins.
5. Partitioned tables with BRIN for a few million rows: not verified against docs, and a few million rows is small. TimescaleDB has two editions. The Apache 2 edition has hypertables, time_bucket, first/last and drop_chunks. The Community edition is under the Tiger Data License (formerly Timescale License) and adds continuous aggregates, the Hypercore columnstore, retention policies, jobs and gapfill. That license allows self-hosting, including production, but forbids offering it as a service. I did not find a documented scale threshold for needing it.
6. Procrastinate is 3.10.0 (GitHub release dated 23 Sep, year not shown) under the MIT license. PGQueuer is MIT, needs PG 14+ and Python 3.11+, and states it uses FOR UPDATE SKIP LOCKED. Its latest version is not found. A PyPI response showing 1.6.0 and 0.26.2 was ambiguous and is not reliable. pgmq has a v1.10.0 image tag, supports PG 14-18 and uses the PostgreSQL license. Its Python client pgmq-py is Apache-2.0. The README lists Tembo only as a user, not as maintainer, and the repo now sits under the `pgmq` org. I found no SKIP LOCKED statement in the pgmq pages (it is not shown in the README). I did not check Celery or Dramatiq: not found.
7. Apache AGE: the latest release is v1.8.0 for PG18 (9 July, year not shown), with a PG15 pre-release. v1.7.0 supported PG17 and PG18, and v1.6.0 supported PG14-17. Releases continue, so it appears maintained. I have no source for the relational adjacency-table / recursive CTE guidance: not found.

## Evidence

- https://www.postgresql.org/support/versioning/ — versions, minors, EOL dates
- https://github.com/pgvector/pgvector — v0.8.7, dimension limits, scaling guidance
- https://github.com/paradedb/paradedb/releases — pg_search v0.26.2
- https://raw.githubusercontent.com/paradedb/paradedb/main/README.md — AGPL-3.0 Community, commercial Enterprise
- https://www.paradedb.com/docs/llms.txt — tokenizer pages (icu, lindera, jieba, chinese-compatible)
- https://www.postgresql.org/docs/current/textsearch-limitations.html — tsvector limits
- https://www.tigerdata.com/docs/about/latest/timescaledb-editions — edition split and license terms
- https://github.com/timescale/pgvectorscale — PostgreSQL license
- https://github.com/apache/age/releases — AGE v1.8.0 PG18
- https://postgis.net/development/source_code/ — PostGIS 3.6.4
- https://github.com/procrastinate-org/procrastinate/releases and https://pypi.org/pypi/procrastinate/json — 3.10.0, MIT
- https://github.com/janbjorge/pgqueuer — MIT, SKIP LOCKED
- https://github.com/pgmq/pgmq and https://github.com/pgmq/pgmq-py — pgmq details

## Caveats (verbatim)

The fetcher is a summarising model, so figures are second-hand and not read from raw pages. Several release dates lack a year. I did not establish the scale thresholds you asked about (Elasticsearch, vectors, TimescaleDB) from any primary source, and the answer should not be read as supporting or refuting them. Items 4, 5 and 7 are mostly "not found".

## Orchestrator note

Nothing here contradicts a single-Postgres design at Canary's scale (a few million documents, a few million embeddings, tens of millions of observations). The scale thresholds are a judgement, recorded as such in `docs/07`: Postgres alone until measured query latency or index build time fails the targets, with pg_search (AGPL, acceptable for a non-profit that publishes its code) as the first upgrade for multilingual BM25 before any OpenSearch cluster is considered.
