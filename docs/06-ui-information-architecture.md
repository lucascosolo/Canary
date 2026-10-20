# 06. UI and information architecture

## 1. Principles that follow from the framework

The interface has one job: let a reader go from "what matters today" to a claim's quoted span in
two clicks, without ever being shown a number that pretends to be a conclusion. Five properties
of any item are shown as five separate channels and never merged into one colour scale:

| Property | Encoding | Never encoded as |
|---|---|---|
| Urgency (how new, how fast) | Position in the list; a "since" stamp; a small motion-free marker for "new in last 24h" | Red |
| Severity (what is at stake) | A short phrase in words ("independence of the highest court") | A score or bar |
| Confidence (evidence × agreement) | The IPCC word plus the two inputs as two small glyph rows (evidence: 1-3 dots; agreement: 1-3 dots) | A percentage |
| Trend (direction) | An arrow with a word: deteriorating, improving, stable, mixed; arrows never coloured by direction alone (WCAG 1.4.1, F-03) | Colour only |
| Completeness (coverage, freshness) | A coverage label (high, medium, low, obscured) and a freshness stamp per source | Hidden |

Colour is reserved for domain (institutions, rights, conflict, information, economy,
humanitarian) and is muted; the palette has no alarm red. Dark and light themes both ship; the
default follows the system. Every map has a table equivalent. Keyboard navigation follows the
WAI-ARIA grid pattern for lists and tables (F-03). Text is set for long reading sessions: a
measure of 60-75 characters in prose panels, dense tabular panels elsewhere.

## 2. The user's mockups, and what Canary takes from them

The two mockups in `design_mockups/` (viewed 2026-10-20) are useful as a statement of taste.
Adopted: the left rail with few, stable destinations; the dark "command center" density of
option 1; the domain tabs; the key-indicator list with sparklines and a change figure; the
narrow right-hand "insights" column with three to five short items; the split of a wide
time-series panel above a dense list; the clean card rhythm and the filter chips of option 2.

Not adopted, with the reason: option 2's "Global Risk Level 846/1000, Elevated" gauge is the
composite score START.md section 7 forbids and document 04 rules out; Canary's right rail instead
shows "What changed", "Coverage gaps" and "Under review" as three labelled lists. Option 2's
photo-led news cards make Canary look like "a conventional news website with a different colour
scheme" (START.md section 9) and tie prominence to image availability, which correlates with
Western coverage; Canary's Today list is text-first, with the eight questions compressed into a
card and a small domain glyph instead of a photograph. Option 2's uniformly red up-arrows encode
"up is bad" for every series, which is false for half of Canary's indicators (an improvement is
also "up"); Canary's arrows carry a word. Option 1's chart of GDP growth by region is a fine
component for the economy tab but would not be the home page: the home page is about change
that needs attention, not a macro chart.

## 3. Views

### 3.1 Today (home)

A single column of attention items, each a compact card rendering the eight questions in fixed
order: a one-line "what happened" with country and date; "why it matters" in one sentence;
confidence (word plus glyphs); trend arrow with word; coverage label; "evidence: N claims from K
independent lineages" as a link; "historical context" as the count of comparisons with the
top one named; "next: ..." with one open question. Items are grouped into three sections with
headings, in this order: reviewed assessments updated in the last seven days (deterioration and
improvement interleaved by recency, not segregated); scheduled things worth watching (elections,
rulings, deadlines in the next 30 days, from the calendar); automated flags not yet reviewed
(collapsed by default, labelled, showing the rule name and the signals). A right rail shows
"What changed since yesterday" (counts by domain, with "no data" where ingestion is stale),
"Coverage gaps" (countries whose coverage label dropped), and "Sources" (health summary: N feeds
fresh, M stale, with a link). Filters: domain, region, direction, confidence, coverage. Nothing
on Today is a number without a unit and a definition on hover.

### 3.2 Map

A tile-free world map (Natural Earth TopoJSON rendered as SVG with D3; no WebGL, no tiles) with country fills
reserved for one chosen property at a time, selected explicitly by the reader: number of
reviewed situations, trend, coverage label, a chosen baseline index with its year, or a chosen
indicator's change signal. The legend states the property, the source and the date. Hovering
shows the country's label row (coverage, situations, last review). No "risk heat map" default.
Disputed territories and non-state areas are drawn as the source draws them, with the source
named. The table equivalent is one click away and carries the same columns.

### 3.3 Country

Header: name, codes, region, coverage label with its five facts on expand, the three layers as
three labelled panels across the top: Baseline (the indices with year and interval, each linked
to its source and licence), Change (the indicator list with sparklines, baseline band and the
latest signal, in the style of option 1's key-indicator list), Assessment (the open situations
with their cards). Below: a timeline of events (reviewed), a feed of claims (with lineage
counts), the sources covering the country (by class and language), scheduled events, and the
episodes in the library involving this country. Every panel has "last updated" and "source".

### 3.4 Situation

The full assessment in the eight-question order, then the evidence record as a table
(claim, quoted span, source, class, independence, category, process-tracing weight,
supports/contradicts), the timeline of the situation's events, the signals that contributed,
the comparisons (each rendered with likenesses, differences, unclear, placement, base rate and
the required sentence), the version history with diffs, and the corrections. "What would change
this assessment" sits at the bottom of the first screen, not the end of the page.

### 3.5 Trends

Cross-country views by domain tab (institutions, elections, legislation, conflict, rights,
information, economy, humanitarian): small multiples of one indicator across chosen countries,
a change-signal board (which countries have an active signal on this indicator, since when),
and the baseline distribution with the chosen country marked. This is where option 1's chart
lives.

### 3.6 History

The episode library: a filterable list by type, region, period and outcome; an episode page with
the time-line, early signs, mechanisms, protective factors and the "what observers misread"
section; a comparison browser showing which current situations have been compared to this
episode; and the base-rate tables with their definitions.

### 3.7 Sources

The public source registry: each source's class, coverage, cadence, licence and attribution
text, freshness, last schema change, consecutive failures, and known limitations in prose.
Filters by domain and country. The page is also the place where readers learn what Canary
cannot see.

### 3.8 Search and archive

Full-text and structured search across claims, events, assessments, episodes and sources, with
filters for country, date range, domain, source class, evidence category, confidence, and
language of the original document. Results keep the original-language title and show the
translation beside it. Saved searches and watchlists are a Phase 4 feature for the operator
first; readers get shareable URLs for any filtered view in Phase 2.

### 3.9 Methodology, calibration and corrections

Three public pages that are part of the product, not an appendix: the framework in document 04
in reader form (layers, evidence categories, confidence table, watch rules in force with their
rationale); the calibration log (false alarms, misses, retired rules, backtest results, document
09); and the corrections log (every change to a published item, with whether the source or
Canary was wrong).

## 4. Progressive disclosure

Level 0 is the Today card (eight questions in eight lines). Level 1 is the situation page's first
screen (full text plus evidence summary). Level 2 is the evidence record and the comparisons.
Level 3 is the raw document view: the original-language text as retrieved (metadata and the
quoted spans; full text only where the licence allows and otherwise the link), the archived copy,
the extraction run's model and prompt version, and the lineage it belongs to. Every level is a
URL.

## 5. Operator workspace

Behind Cloudflare Access (the operator only): the review queue (flags and extracted claims
awaiting support check, ordered by rule and country), the assessment editor with the eight-field
form and the review checklist, the comparison editor with the Neustadt-May fields, the episode
editor, the source registry editor with the licence verification date, the ingestion health
board, and the calibration log entry form. The editor shows Claude drafts as drafts with every
sentence linked to a claim identifier; unsupported sentences cannot be saved.

## 6. Accessibility and performance

WCAG 2.2 AA as the bar (1.4.1 use of colour, 2.4.7 focus visible, 2.4.11 focus not obscured;
F-03). Keyboard: the Today list, tables and the map's table equivalent follow the APG grid
pattern. Mobile: single column, Today first, map behind a tab, sparklines sized for touch.
Performance budget: pages server-rendered from Jinja2 templates with HTMX partial updates
(document 07); first screen of Today under 150 KB transferred excluding fonts; the map and the
chart library loaded only on the pages that use them. Readers are not tracked
beyond aggregate server logs.

## 7. Configurability

A carefully designed default beats configuration at first. Readers get filters and shareable
URLs; the operator gets per-source and per-rule configuration in files. Personal dashboards,
alerts and accounts are not in the first three phases.
