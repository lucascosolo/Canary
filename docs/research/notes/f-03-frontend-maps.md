# F-03: Frontend frameworks, map libraries, tile sources, charts, accessibility

- Date: 2026-10-20
- Agent: researcher (Sonnet, low effort), 8 tool uses (npm registry "latest" dist-tags)

## Answer (verbatim; read 2026-10-20; format name | version | date | license | note)

1. Frameworks
- Svelte | 5.57.2 | 2026-10-06 | MIT | current
- SvelteKit | 3.1.0 | 2026-10-14 | MIT | 3.x is latest, not 2.x
- Next.js | 16.4.2 | 2026-10-15 | MIT | 16 is current
- React | 19.3.1 | 2026-10-14 | MIT | current
- Vue | 3.5.44 | 2026-10-13 | MIT | 3.6 is in rc (3.6.0-rc.12)
- Nuxt | 4.6.2 | 2026-10-16 | MIT | 4 is stable
- htmx.org | 2.0.11 | 2026-09-22 | 0BSD | 4.0.0 is on the "next" tag
- Alpine.js | 3.17.4 | 2026-09-21 | MIT | current
- Astro | 7.4.1 | 2026-10-19 | MIT | latest is 7.x, not 5.x
- Vite | 8.3.4 | 2026-10-08 | MIT | latest is 8.x, not 7.x
- TypeScript | 7.0.2 | 2026-07-08 | Apache-2.0 | latest is 7.x, not 5.x
2. Maps
- MapLibre GL JS | 6.15.0 | 2026-10-18 | BSD-3-Clause | 6.x, not 5.x
- deck.gl | 9.4.0 | 2026-09-05 | MIT | the 4.0.0-rc tag is not the deck.gl 9 line
- Leaflet | 1.9.4 | 2023-05-18 | BSD-2-Clause | 2.0 only reached alpha.1 (2025-08-16); 1.x is stagnant
- OpenLayers (ol) | 10.11.0 | 2026-10-04 | BSD-2-Clause | active
- world-atlas | 2.0.2 | 2019-09-05 | ISC | unchanged for years; I did not read its licence or data terms
- pmtiles (JS) | 4.5.0 | 2026-08-10 | BSD-3-Clause | active
- Tile sources
  - OpenFreeMap: the quick-start page gives the credit "OpenFreeMap © OpenMapTiles Data from OpenStreetMap" with links. It states no licence or commercial-use terms; the ToS page (/tos/) was not read. Limits apply only to offline downloads (3,000 tiles or 50 MB each, 4 parallel requests, unique User-Agent). A modified style must be self-hosted.
  - Protomaps basemap: an ODbL Produced Work, and OSM attribution is required. The full planet file is about 120 GB. The docs say to copy it to your own storage rather than hotlink.
  - Stadia, MapTiler, OpenMapTiles licensing, Natural Earth terms: not found (not read).
3. Charts and tables
- Observable Plot | 0.6.17 | 2025-02-14 | ISC | still 0.6.x
- ECharts | 6.1.0 | 2026-05-19 | Apache-2.0 | 6.x
- D3 | 7.9.0 | 2024-03-12 | ISC | 7.x; the "next" tag is 6.0.0-rc.4, which is stale
- Vega-Lite | 6.5.0 | 2026-10-08 | BSD-3-Clause | 6.x
- TanStack Table (table-core) | 9.3.1 | 2026-10-12 | MIT | 9.x is latest; the last 8.x is 8.21.3 (2025-04-14)
- AG Grid Community | 36.2.0 | 2026-09-16 | MIT | The npm license field says MIT. Enterprise is a separate commercial licence; I did not read its docs.
4. Accessibility and density
(a) The APG grid pattern has these keys: arrows move one cell; Home/End and Ctrl+Home/End jump; PageUp/PageDown move by an author-set row count; Enter/F2 enters a cell's widget and Esc returns. Only one element is in the tab sequence (roving focus). The page does not mention treegrid. The treegrid pattern is at https://www.w3.org/WAI/ARIA/apg/patterns/treegrid/ (not read).
(b) WCAG 2.2 1.4.1 Use of Color (Level A): colour must not be the only means of conveying status, so add text, icon or shape. 2.4.11 Focus Not Obscured (Minimum) (AA): a focused element must not be entirely hidden by sticky headers or overlays. Focus visibility itself is 2.4.7 (AA); 2.4.13 Focus Appearance is AAA. These two points are from memory, not read this session.
(c) Map accessibility guidance: not found. The MapLibre docs landing page has no accessibility section. Treat the map as supplementary and provide a table or list equivalent of its data.

## Evidence

- https://registry.npmjs.org/<pkg> for all 23 packages above (including @tanstack/table-core and the leaflet dist-tags) — versions, dates and licence fields
- https://openfreemap.org/quick_start/ — attribution string and offline limits
- https://docs.protomaps.com/basemaps/downloads — ODbL Produced Work, OSM attribution
- https://www.w3.org/WAI/ARIA/apg/patterns/grid/ — grid keyboard model
- https://maplibre.org/maplibre-gl-js/docs/ — no a11y guidance found

## Caveats (verbatim)

Your assumed versions were mostly stale: SvelteKit 3, Astro 7, Vite 8, TypeScript 7, MapLibre 6, Next 16, TanStack Table 9. The npm "latest" tag is not the same as a vendor announcement, and I did not read GitHub release notes or breaking-change lists. Several of those majors may need migration work before a small team adopts them. The license values are the npm metadata fields only. WCAG points and the Natural Earth public-domain status were not verified from primary pages this session.

## Orchestrator note

The agent corrected my version assumptions, which is the point of looking them up. For `docs/07`: MapLibre 6 with self-hosted Protomaps PMTiles (ODbL produced work, OSM attribution) or OpenFreeMap tiles for the basemap, a tile-free TopoJSON world map as the default global view (Natural Earth is public domain per note A-05), and a table equivalent for every map (the map is supplementary for accessibility). Framework choice is argued in `docs/07`; all candidates are MIT and current.
