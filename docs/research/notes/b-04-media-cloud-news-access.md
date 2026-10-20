# B-04: Media Cloud, Common Crawl News, commercial news APIs, Google News RSS

- Date: 2026-10-20
- Agent: researcher (Sonnet, low effort), 25 tool uses

## Answer (verbatim; all pages read 2026-10-20)

1. Media Cloud: active. The GitHub org shows commits through Oct 2026, and mediacloud.org says the archive holds over 1 billion stories from over 25,000 sources. The API (v4) is wrapped by the `api-client` Python package: `SearchApi.story_list` (query with boolean syntax, start_date/end_date, collection_ids, pagination_token) and `DirectoryApi.source_list` (sources in a collection). A separate count endpoint was not found in the README; its example counts by paging story_list. Full text: not stated (the README and search guide only mention story metadata and, for the Wayback search, "title text"). Access: sign up at search.mediacloud.org for an API key. Rate limits: not found. Current platform repos: api-client, web-search (the search.mediacloud.org tool), story-indexer (ingest pipeline), rss-fetcher, feed_seeker, metadata-lib, mc-providers, es-tools, system-dev-ops, collection-review-tool. 52 of the 62 repos were not listed. A country directory exists in the web tool but I did not fetch it. Terms of use: not found (the footer link exists, but the URLs I tried returned 404).

2. CC-NEWS: daily WARC files at s3://commoncrawl/crawl-data/CC-NEWS/YYYY/MM/CC-NEWS-<timestamp>-<seq>.warc.gz, with per-month file lists at data.commoncrawl.org/crawl-data/CC-NEWS/index.html, from 2016 onward. Size per day and language coverage: not found (only "news sites all over the world"). Common Crawl Terms of Use do NOT assert a copyright status. They say crawled content "may be subject to separate terms of use or terms of service from the owners", that you "evaluate, and bear all risks", and that you "agree to respect the copyrights and other applicable rights of third parties". The licence is to access and use the service. The terms do not explicitly address storing or redistributing extracted text, and they require indemnifying Common Crawl for AI/ML uses (Section 9). So storage is not forbidden or granted explicitly; the copyright risk is yours.

3. Commercial APIs:
- NewsAPI.org: free Developer plan is 100 requests/day, 24h article delay, 1 month history, and dev/testing only ("cannot be used in a staging or production environment (including internally)"). Cheapest paid is Business at $449/month. No full text on any plan (URL plus snippet). Its terms allow keeping downloaded materials "for as long as your use case requires", but forbid making data public without authorisation, "reproduce or republish copyrighted material", and building a competing news database. Language and country coverage: not found.
- GNews.io: free is 100 requests/day, 10 articles/request, 12h delay, 30 days history, truncated content, non-commercial. Cheapest paid is Essential at EUR 49.99/month (EUR 39.99 on yearly billing), with full content. It claims over 80,000 sources; language and country lists were not found. Terms clause: not found (404).
- NewsData.io: pricing and terms pages returned only a title (JS-rendered), so free tier, price, full text and terms are all not found.

4. Google News RSS: no RSS-specific terms found. Google ToS (policies.google.com/terms) prohibit "using automated means to access content from any of our services" in violation of machine-readable instructions such as robots.txt, and allow suspension for "scraping content that doesn't belong to you".

## Evidence

- https://github.com/mediacloud — repo list, activity dates
- https://github.com/mediacloud/api-client — v4 API, key from search.mediacloud.org
- https://www.mediacloud.org/ — scale figures
- https://www.mediacloud.org/documentation/search-api-guide — no endpoint, rate-limit or key detail
- https://commoncrawl.org/terms-of-use — Sections 1-3, 9
- https://commoncrawl.org/blog/news-dataset-available — S3 path, file layout
- https://newsapi.org/pricing and https://newsapi.org/terms — limits and clauses
- https://gnews.io/pricing and https://docs.gnews.io/ — limits, full content
- https://policies.google.com/terms — automated access clause

## Caveats (verbatim)

Fetches were summarised by a small model, not read verbatim. Missing: the Media Cloud terms, rate limits, full-text status and country directory; CC-NEWS daily size and languages; all NewsData.io data; the GNews terms. The api-client README license badge conflicts with the repo's Apache-2.0 licence. Prices were those shown on the page on 2026-10-20 and are not otherwise verified.

## Orchestrator note

Two conclusions follow. First, no affordable commercial news API returns full text with redistribution rights; the project's news layer must be built on publishers' own RSS feeds, Media Cloud's story metadata, GDELT's URL-level signals and, for text, fetching the article itself under the publisher's terms and storing only what copyright permits (metadata, short excerpts, extracted claims). Second, Media Cloud's open-source `rss-fetcher`, `feed_seeker` and `story-indexer` are candidate components to reuse rather than rebuild.
