# 08. Data model and schemas

Entities are listed with their purpose, the fields that matter to the design, and their write
rule. Exact column types and indexes are for the first implementation phase to settle in Alembic
migrations; what is fixed here is which entities exist, how provenance flows between them, and
what may never be overwritten. Identifiers are UUIDv7 (time-ordered). Timestamps are UTC with
offset. Country references carry ISO 3166-1 alpha-3 plus a Natural Earth or GeoNames id for
territories and disputed areas. Enumerations are lowercase snake_case from fixed sets held in
versioned vocabulary files.

## 1. Provenance spine

- **pipeline_run** (append-only): `id`, `stage` (ingest, normalise, extract, support_check,
  lineage, event_assembly, indicator, baseline, change_detection, watch_rules, coverage,
  embed, translate, draft), `started_at`, `ended_at`, `code_commit`, `config_digest`,
  `model_id`, `prompt_version`, `schema_version`, `indicator_catalog_version`,
  `rule_file_version`, `input_count`, `output_count`, `error_count`, `notes`. Every derived row
  points to the run that made it. Re-running with identical versions must reproduce outputs
  (document 07, section 11).

## 2. Sources and documents

- **source** (editorial, versioned): the registry record of document 03, section 7, plus
  `current_version`. Changes create `source_version` rows; the runtime health fields live in
  **source_health** (append-only samples: `checked_at`, `ok`, `latency_ms`, `items_seen`,
  `schema_digest`, `message`).
- **document** (append-only): `id`, `source_id`, `url`, `canonical_url`, `retrieved_at`,
  `published_at` (as stated by the source; nullable), `published_at_precision`, `http_status`,
  `content_type`, `raw_ref` (file digest and path), `raw_digest`, `title_original`,
  `language` (detected, with confidence), `text_ref` (normalised text version), `text_digest`,
  `licence_mode` (what may be stored and shown: metadata_only, excerpt, full), `archive_url`
  (Internet Archive capture at retrieval), `adapter_version`, `run_id`. A document is never
  edited; a re-fetch is a new document row linked by `supersedes_document_id`, which is how a
  source's own correction is recorded.
- **document_text** (append-only per normaliser version): `document_id`, `normaliser_version`,
  `text`, `paragraph_offsets`, `run_id`. Stored only where `licence_mode` allows; otherwise only
  the quoted spans survive in claims.
- **document_translation** (append-only): `document_id`, `field` (title, span), `span_ref`,
  `target_language`, `text`, `engine` (madlad, claude), `engine_version`, `run_id`.
- **dataset_release** (append-only): `source_id`, `version_label`, `released_at` (stated),
  `retrieved_at`, `file_refs`, `row_count`, `schema_digest`, `licence_snapshot`, `run_id`.

## 3. Claims, lineages, events

- **claim** (append-only; status changes are new rows via `claim_status`): `id`, `document_id`,
  `run_id`, `claim_type` (from the vocabulary: an adapted PLOVER core plus Canary's
  institutional-integrity, rights, information-control and resilience types), `polarity`
  (deterioration, improvement, neutral), `actor_ref` (Wikidata id or curated alias id, plus the
  surface string), `actor_class` (government, executive, legislature, court, election_body,
  security_force, party, media, civil_society, armed_group, foreign_state, intergovernmental,
  individual_public), `target_ref`, `target_class`, `place_ref` (GeoNames or country), `place_precision`,
  `event_time` (interval with precision), `quoted_span` (verbatim), `span_offsets`,
  `span_language`, `evidence_category` (the twelve values of document 04, section 2),
  `extraction_confidence` (the model's own, stored but never shown as a probability),
  `support_check` (pending, passed, failed), `support_check_run_id`.
- **claim_status** (append-only): `claim_id`, `status` (candidate, accepted, rejected,
  superseded), `reason`, `actor` (system or operator id), `at`.
- **lineage** (append-only; membership rows append): `id`, `origin_class` (official_statement,
  wire, single_outlet, ngo_report, court_document, dataset, unknown), `origin_source_id`,
  `earliest_document_id`, `method` (minhash, attribution, quote_match, manual), `run_id`;
  **lineage_member**: `lineage_id`, `document_id`, `similarity`, `run_id`.
- **event** (versioned): `id`, `event_type`, `country`, `place_ref`, `event_time`,
  `summary` (operator or rule text), `assembled_by` (rule name or operator), `single_sourced`
  (true when fewer than two independent lineages), `version`, `run_id`; **event_claim**:
  `event_id`, `claim_id`, `role` (supports, contradicts, context).
- **actor** (editorial): curated alias table: `id`, `wikidata_id`, `names` (by language),
  `actor_class`, `country`, `active_from`, `active_to`, `notes`.
- **place** (reference): GeoNames and Natural Earth joins; `disputed` flag with the source's
  framing recorded as text.

## 4. Indicators and observations

- **indicator** (editorial, versioned): `id`, `name`, `definition`, `domain`, `source_id`,
  `unit`, `cadence`, `deterioration_direction` (up, down, none), `baseline_method`,
  `detection_method`, `detection_params`, `reporting_bias_note`, `licence_mode`, `version`.
- **observation** (append-only, partitioned by month): `indicator_id`, `geo_ref`, `period_start`,
  `period_end`, `value`, `value_low`, `value_high` (intervals where the source gives them),
  `vintage_release_id`, `retrieved_at`, `run_id`. A revised value is a new row with a later
  vintage; queries "as of date D" take the latest vintage retrieved before D.
- **baseline** (append-only): `indicator_id`, `geo_ref`, `horizon` (12m, 5y, full),
  `computed_at`, `stats` (JSON: mean, dispersion, trend, seasonal terms), `method_version`,
  `run_id`.
- **signal** (append-only): `id`, `indicator_id`, `geo_ref`, `window_start`, `window_end`,
  `method`, `method_version`, `statistic`, `threshold`, `baseline_id`, `direction`,
  `coverage_label_at_time`, `run_id`.
- **coverage_index** (append-only, monthly): `country`, `month`, `active_sources_by_class`,
  `languages`, `baseline_docs_per_day`, `current_docs_per_day`, `information_control_active`,
  `indicators_with_current_observation_share`, `last_human_review_at`, `label` (high, medium,
  low, obscured), `rule_version`, `run_id`.

## 5. Rules, flags, situations, assessments

- **watch_rule** (editorial, versioned from the rule file): `name`, `version`, `rationale`,
  `scope`, `window`, `conditions` (structured), `strengthen_text`, `weaken_text`,
  `withdraw_text`, `enabled`, `enabled_from`.
- **flag** (append-only): `id`, `rule_name`, `rule_version`, `country`, `situation_id` (nullable
  until linked), `fired_at`, `signal_ids`, `claim_ids`, `baseline_snapshot`, `status`
  (unreviewed, reviewed_accepted, reviewed_rejected, expired), `review_note`, `reviewer`,
  `reviewed_at`, `run_id`.
- **situation** (editorial): `id`, `country`, `theme` (domain plus subject), `title`,
  `opened_at`, `closed_at`, `status` (open, watching, closed_improved, closed_stable,
  closed_merged), `current_assessment_id`.
- **assessment** (versioned, append-only versions): `id`, `situation_id`, `version`,
  `what_happened`, `where_when` (structured), `why_it_matters`, `direction`
  (deteriorating, improving, stable_dangerous, mixed), `severity_text`, `atrocity_factor_refs`
  (UN Framework factors, nullable), `evidence_amount` (limited, medium, robust),
  `source_agreement` (low, medium, high), `confidence` (derived, stored for audit),
  `model_quote` (nullable: external model, value, base rate, precision, url),
  `investigate_next`, `change_conditions` (raise, lower, withdraw texts), `drafted_by`
  (operator or model id with prompt version), `approved_by`, `approved_at`, `review_checklist`
  (completed items), `published_at`, `run_id`.
- **evidence_link** (append-only per assessment version): `assessment_id`, `assessment_version`,
  `item_type` (claim, event, observation, signal, document), `item_id`, `role` (supports,
  contradicts, qualifies), `evidence_category`, `process_tracing_weight`,
  `source_reliability_letter`, `information_credibility_digit`, `note`.
- **missing_evidence** (per assessment version): `assessment_id`, `assessment_version`, `text`.

## 6. History

- **episode** (editorial, versioned): fields of document 05, section 2; `ert_episode_id`,
  `gwf_regime_id` nullable; `outcome`; `reviewed_by`.
- **episode_milestone** (versioned with the episode): `episode_id`, `date`, `date_precision`,
  `institution_or_right`, `text`, `claim_type`, `sources` (citations with URLs or DOIs),
  `early_sign` (bool), `lead_time_days` (nullable).
- **episode_feature** (derived from the editorial record for matching): `episode_id`, `feature`
  (type, institutions affected, first-three-milestone order, regime type, baseline quartiles,
  protective factors), `value`.
- **comparison** (versioned with the assessment): `situation_id`, `assessment_version`,
  `episode_id`, `known`, `unknown`, `presumed`, `likenesses`, `differences`, `unclear`,
  `placement`, `episode_position_milestone_id`, `reference_class`, `base_rate_text`,
  `base_rate_dataset_version`, `author`, `retired_at`.

## 7. Corrections and audit

- **correction** (append-only): `id`, `item_type`, `item_id`, `item_version_before`,
  `item_version_after`, `kind` (source_corrected, canary_processing_error, canary_editorial_error,
  clarification), `description`, `public` (bool, default true), `made_by`, `made_at`.
  A source correcting its record (the CPJ removals, a dataset revision) is `source_corrected`
  and links the superseding document or vintage; Canary's own mistakes are the other kinds. The
  corrections page renders this table.
- **editorial_audit** (append-only): every operator action with actor, time, item, diff ref.
- **calibration_entry** (append-only): `kind` (false_alarm, miss, late, rule_retired,
  backtest_result, comparison_misread), `refs`, `description`, `metric_values`, `made_at`;
  rendered as the calibration log.

## 8. Rules that bind every table

1. Nothing in raw, derived or append-only tables is updated or deleted by application code;
   supersession is a new row with a pointer. The database roles enforce this (document 07).
2. Every derived row carries `run_id`; every editorial row carries `version` and the actor.
3. Every displayed value can be traced in two joins to a document, a dataset release or an
   operator action.
4. Enumerations come from vocabulary files under version control; adding a value is a commit.
5. Vintage is mandatory on observations; "as of" queries are a first-class query helper used by
   the backtests.
6. Licence mode on documents and indicators is checked at render time; the renderer refuses to
   show a field the mode does not allow.

## 9. What is intentionally not modelled yet

Reader accounts, watchlists and alerts; a general knowledge graph of relationships between
actors (the alias table and Wikidata ids are enough for linking; relationship edges wait for a
use case); subnational administrative time series beyond what sources provide geocoded; a
legislation entity with full lifecycle for every country (document 03 shows the data does not
exist globally; the claim vocabulary carries bill-stage types, and a `legislation` entity is
added in Phase 4 for the jurisdictions with APIs).
