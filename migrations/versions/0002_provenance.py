# ruff: noqa: E501
"""Provenance spine: run, source, version, health and release tables with write-rule triggers.

Revision ID: 0002
Revises: 0001
"""

import sqlalchemy as sa
from alembic import op
from sqlalchemy.dialects import postgresql

revision = "0002"
down_revision = "0001"
branch_labels = None
depends_on = None

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

TS = sa.DateTime(timezone=True)
UUID = postgresql.UUID(as_uuid=True)

REFUSE_FUNCTION = """
create function canary_refuse() returns trigger language plpgsql as $$
begin
    raise exception '% on % is refused: the provenance record is append-only', TG_OP, TG_TABLE_NAME
        using errcode = 'integrity_constraint_violation';
end
$$
"""

RUN_UPDATE_FUNCTION = """
create function canary_run_update() returns trigger language plpgsql as $$
begin
    if OLD.ended_at is not null or NEW.ended_at is null then
        raise exception 'UPDATE on pipeline_run is refused: only closing an open run is allowed'
            using errcode = 'integrity_constraint_violation';
    end if;
    if (NEW.id, NEW.stage, NEW.started_at, NEW.code_commit, NEW.config_digest, NEW.model_id,
        NEW.prompt_version, NEW.schema_version, NEW.indicator_catalog_version,
        NEW.rule_file_version)
        is distinct from
       (OLD.id, OLD.stage, OLD.started_at, OLD.code_commit, OLD.config_digest, OLD.model_id,
        OLD.prompt_version, OLD.schema_version, OLD.indicator_catalog_version,
        OLD.rule_file_version) then
        raise exception 'UPDATE on pipeline_run is refused: only ended_at, counts and notes change'
            using errcode = 'integrity_constraint_violation';
    end if;
    return NEW;
end
$$
"""


def upgrade() -> None:
    op.create_table(
        "pipeline_run",
        sa.Column("id", UUID, primary_key=True),
        sa.Column("stage", sa.Text, nullable=False),
        sa.Column("started_at", TS, nullable=False),
        sa.Column("ended_at", TS),
        sa.Column("code_commit", sa.Text, nullable=False),
        sa.Column("config_digest", sa.Text, nullable=False),
        sa.Column("model_id", sa.Text),
        sa.Column("prompt_version", sa.Text),
        sa.Column("schema_version", sa.Text),
        sa.Column("indicator_catalog_version", sa.Text),
        sa.Column("rule_file_version", sa.Text),
        sa.Column("notes", sa.Text),
        sa.Column("input_count", sa.Integer, nullable=False, server_default="0"),
        sa.Column("output_count", sa.Integer, nullable=False, server_default="0"),
        sa.Column("error_count", sa.Integer, nullable=False, server_default="0"),
        sa.CheckConstraint(
            "stage in (" + ", ".join(f"'{s}'" for s in STAGES) + ")",
            name="pipeline_run_stage_check",
        ),
    )
    op.create_table(
        "source",
        sa.Column("id", sa.Text, primary_key=True),
        sa.Column("current_version", sa.Integer, nullable=False),
        sa.Column("canary_use", sa.Text, nullable=False),
        sa.Column("status", sa.Text, nullable=False),
        sa.Column("record", postgresql.JSONB, nullable=False),
    )
    op.create_table(
        "source_version",
        sa.Column("source_id", sa.Text, sa.ForeignKey("source.id"), nullable=False),
        sa.Column("version", sa.Integer, nullable=False),
        sa.Column("record", postgresql.JSONB, nullable=False),
        sa.Column("digest", sa.Text, nullable=False),
        sa.Column("run_id", UUID, sa.ForeignKey("pipeline_run.id"), nullable=False),
        sa.Column("recorded_at", TS, nullable=False),
        sa.PrimaryKeyConstraint("source_id", "version"),
    )
    op.create_table(
        "source_health",
        sa.Column("id", UUID, primary_key=True),
        sa.Column("source_id", sa.Text, sa.ForeignKey("source.id"), nullable=False),
        sa.Column("checked_at", TS, nullable=False),
        sa.Column("ok", sa.Boolean, nullable=False),
        sa.Column("latency_ms", sa.Integer),
        sa.Column("items_seen", sa.Integer),
        sa.Column("schema_digest", sa.Text),
        sa.Column("message", sa.Text),
    )
    op.create_table(
        "dataset_release",
        sa.Column("id", UUID, primary_key=True),
        sa.Column("source_id", sa.Text, sa.ForeignKey("source.id"), nullable=False),
        sa.Column("version_label", sa.Text, nullable=False),
        sa.Column("released_at", TS),
        sa.Column("retrieved_at", TS, nullable=False),
        sa.Column("file_refs", postgresql.JSONB, nullable=False),
        sa.Column("content_digest", sa.Text, nullable=False),
        sa.Column("row_count", sa.Integer, nullable=False),
        sa.Column("schema_digest", sa.Text, nullable=False),
        sa.Column("licence_snapshot", sa.Text, nullable=False),
        sa.Column("run_id", UUID, sa.ForeignKey("pipeline_run.id"), nullable=False),
        sa.UniqueConstraint("source_id", "content_digest", name="dataset_release_source_digest_key"),
    )

    op.execute(REFUSE_FUNCTION)
    op.execute(RUN_UPDATE_FUNCTION)

    op.execute("create trigger source_version_no_update before update on source_version for each row execute function canary_refuse()")  # SAFETY-GUARD
    op.execute("create trigger source_health_no_update before update on source_health for each row execute function canary_refuse()")  # SAFETY-GUARD
    op.execute("create trigger dataset_release_no_update before update on dataset_release for each row execute function canary_refuse()")  # SAFETY-GUARD
    op.execute("create trigger pipeline_run_close_only before update on pipeline_run for each row execute function canary_run_update()")  # SAFETY-GUARD

    op.execute("create trigger source_no_delete before delete on source for each statement execute function canary_refuse()")  # SAFETY-GUARD
    op.execute("create trigger pipeline_run_no_delete before delete on pipeline_run for each statement execute function canary_refuse()")  # SAFETY-GUARD
    op.execute("create trigger source_version_no_delete before delete on source_version for each statement execute function canary_refuse()")  # SAFETY-GUARD
    op.execute("create trigger source_health_no_delete before delete on source_health for each statement execute function canary_refuse()")  # SAFETY-GUARD
    op.execute("create trigger dataset_release_no_delete before delete on dataset_release for each statement execute function canary_refuse()")  # SAFETY-GUARD

    op.execute("create trigger source_no_truncate before truncate on source for each statement execute function canary_refuse()")  # SAFETY-GUARD
    op.execute("create trigger pipeline_run_no_truncate before truncate on pipeline_run for each statement execute function canary_refuse()")  # SAFETY-GUARD
    op.execute("create trigger source_version_no_truncate before truncate on source_version for each statement execute function canary_refuse()")  # SAFETY-GUARD
    op.execute("create trigger source_health_no_truncate before truncate on source_health for each statement execute function canary_refuse()")  # SAFETY-GUARD
    op.execute("create trigger dataset_release_no_truncate before truncate on dataset_release for each statement execute function canary_refuse()")  # SAFETY-GUARD


def downgrade() -> None:
    raise NotImplementedError("0002 holds provenance records; it is never undone by a migration")
