"""SQLAlchemy Core metadata for the provenance spine. Migration 0002 creates these tables."""

from __future__ import annotations

from sqlalchemy import (
    Boolean,
    CheckConstraint,
    Column,
    ForeignKey,
    Integer,
    MetaData,
    PrimaryKeyConstraint,
    Table,
    Text,
    UniqueConstraint,
)
from sqlalchemy.dialects.postgresql import JSONB, UUID
from sqlalchemy.types import DateTime

STAGES = (
    "ingest",
    "normalise",
    "extract",
    "support_check",
    "lineage",
    "event_assembly",
    "indicator",
    "baseline",
    "change_detection",
    "watch_rules",
    "coverage",
    "embed",
    "translate",
    "draft",
)

metadata = MetaData()

_TS = DateTime(timezone=True)

pipeline_run = Table(
    "pipeline_run",
    metadata,
    Column("id", UUID(as_uuid=True), primary_key=True),
    Column("stage", Text, nullable=False),
    Column("started_at", _TS, nullable=False),
    Column("ended_at", _TS),
    Column("code_commit", Text, nullable=False),
    Column("config_digest", Text, nullable=False),
    Column("model_id", Text),
    Column("prompt_version", Text),
    Column("schema_version", Text),
    Column("indicator_catalog_version", Text),
    Column("rule_file_version", Text),
    Column("notes", Text),
    Column("input_count", Integer, nullable=False, server_default="0"),
    Column("output_count", Integer, nullable=False, server_default="0"),
    Column("error_count", Integer, nullable=False, server_default="0"),
    CheckConstraint(
        "stage in (" + ", ".join(f"'{s}'" for s in STAGES) + ")", name="pipeline_run_stage_check"
    ),
)

source = Table(
    "source",
    metadata,
    Column("id", Text, primary_key=True),
    Column("current_version", Integer, nullable=False),
    Column("canary_use", Text, nullable=False),
    Column("status", Text, nullable=False),
    Column("record", JSONB, nullable=False),
)

source_version = Table(
    "source_version",
    metadata,
    Column("source_id", Text, ForeignKey("source.id"), nullable=False),
    Column("version", Integer, nullable=False),
    Column("record", JSONB, nullable=False),
    Column("digest", Text, nullable=False),
    Column("run_id", UUID(as_uuid=True), ForeignKey("pipeline_run.id"), nullable=False),
    Column("recorded_at", _TS, nullable=False),
    PrimaryKeyConstraint("source_id", "version"),
)

source_health = Table(
    "source_health",
    metadata,
    Column("id", UUID(as_uuid=True), primary_key=True),
    Column("source_id", Text, ForeignKey("source.id"), nullable=False),
    Column("checked_at", _TS, nullable=False),
    Column("ok", Boolean, nullable=False),
    Column("latency_ms", Integer),
    Column("items_seen", Integer),
    Column("schema_digest", Text),
    Column("message", Text),
)

dataset_release = Table(
    "dataset_release",
    metadata,
    Column("id", UUID(as_uuid=True), primary_key=True),
    Column("source_id", Text, ForeignKey("source.id"), nullable=False),
    Column("version_label", Text, nullable=False),
    Column("released_at", _TS),
    Column("retrieved_at", _TS, nullable=False),
    Column("file_refs", JSONB, nullable=False),
    Column("content_digest", Text, nullable=False),
    Column("row_count", Integer, nullable=False),
    Column("schema_digest", Text, nullable=False),
    Column("licence_snapshot", Text, nullable=False),
    Column("run_id", UUID(as_uuid=True), ForeignKey("pipeline_run.id"), nullable=False),
    UniqueConstraint("source_id", "content_digest", name="dataset_release_source_digest_key"),
)
