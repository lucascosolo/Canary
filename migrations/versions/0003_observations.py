# ruff: noqa: E501
"""Observations with vintages: indicator, indicator_version, observation (partitioned), baseline.

Revision ID: 0003
Revises: 0002
"""

import sqlalchemy as sa
from alembic import op
from sqlalchemy.dialects import postgresql

revision = "0003"
down_revision = "0002"
branch_labels = None
depends_on = None

TS = sa.DateTime(timezone=True)
UUID = postgresql.UUID(as_uuid=True)


def upgrade() -> None:
    op.create_table(
        "indicator",
        sa.Column("id", sa.Text, primary_key=True),
        sa.Column("current_version", sa.Integer, nullable=False),
        sa.Column("source_id", sa.Text, sa.ForeignKey("source.id"), nullable=False),
        sa.Column("record", postgresql.JSONB, nullable=False),
    )
    op.create_table(
        "indicator_version",
        sa.Column("indicator_id", sa.Text, sa.ForeignKey("indicator.id"), nullable=False),
        sa.Column("version", sa.Integer, nullable=False),
        sa.Column("record", postgresql.JSONB, nullable=False),
        sa.Column("digest", sa.Text, nullable=False),
        sa.Column("recorded_at", TS, nullable=False),
        sa.Column("run_id", UUID, sa.ForeignKey("pipeline_run.id"), nullable=False),
        sa.PrimaryKeyConstraint("indicator_id", "version"),
    )
    op.create_table(
        "observation",
        sa.Column("id", UUID, nullable=False),
        sa.Column("indicator_id", sa.Text, sa.ForeignKey("indicator.id"), nullable=False),
        sa.Column("geo_ref", sa.Text, nullable=False),
        sa.Column("period_start", sa.Date, nullable=False),
        sa.Column("period_end", sa.Date, nullable=False),
        sa.Column("value", sa.Double, nullable=False),
        sa.Column("value_low", sa.Double),
        sa.Column("value_high", sa.Double),
        sa.Column("vintage_release_id", UUID, sa.ForeignKey("dataset_release.id"), nullable=False),
        sa.Column("retrieved_at", TS, nullable=False),
        sa.Column("run_id", UUID, sa.ForeignKey("pipeline_run.id"), nullable=False),
        sa.PrimaryKeyConstraint("id", "retrieved_at"),
        sa.CheckConstraint("period_end >= period_start", name="observation_period_check"),
        postgresql_partition_by="RANGE (retrieved_at)",
    )
    op.create_index(
        "observation_key_idx",
        "observation",
        ["indicator_id", "geo_ref", "period_start", "retrieved_at"],
    )
    op.create_table(
        "baseline",
        sa.Column("id", UUID, primary_key=True),
        sa.Column("indicator_id", sa.Text, sa.ForeignKey("indicator.id"), nullable=False),
        sa.Column("geo_ref", sa.Text, nullable=False),
        sa.Column("horizon", sa.Text, nullable=False),
        sa.Column("computed_at", TS, nullable=False),
        sa.Column("stats", postgresql.JSONB, nullable=False),
        sa.Column("method_version", sa.Text, nullable=False),
        sa.Column("run_id", UUID, sa.ForeignKey("pipeline_run.id"), nullable=False),
        sa.CheckConstraint("horizon in ('12m', '5y', 'full')", name="baseline_horizon_check"),
    )

    each_row = "for each row execute function canary_refuse()"
    each_statement = "for each statement execute function canary_refuse()"

    op.execute("create trigger indicator_no_delete before delete on indicator " + each_statement)  # SAFETY-GUARD
    op.execute("create trigger indicator_no_truncate before truncate on indicator " + each_statement)  # SAFETY-GUARD

    op.execute("create trigger indicator_version_no_update before update on indicator_version " + each_row)  # SAFETY-GUARD
    op.execute("create trigger indicator_version_no_delete before delete on indicator_version " + each_statement)  # SAFETY-GUARD
    op.execute("create trigger indicator_version_no_truncate before truncate on indicator_version " + each_statement)  # SAFETY-GUARD

    op.execute("create trigger baseline_no_update before update on baseline " + each_row)  # SAFETY-GUARD
    op.execute("create trigger baseline_no_delete before delete on baseline " + each_statement)  # SAFETY-GUARD
    op.execute("create trigger baseline_no_truncate before truncate on baseline " + each_statement)  # SAFETY-GUARD

    op.execute("create trigger observation_no_update before update on observation " + each_row)  # SAFETY-GUARD
    op.execute("create trigger observation_no_delete before delete on observation " + each_row)  # SAFETY-GUARD
    op.execute("create trigger observation_no_truncate before truncate on observation " + each_statement)  # SAFETY-GUARD


def downgrade() -> None:
    raise NotImplementedError("0003 holds observation records; it is never undone by a migration")
