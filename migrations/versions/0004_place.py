# ruff: noqa: E501
"""The place table: countries from GeoNames, with Wikidata identifiers.

Revision ID: 0004
Revises: 0003
"""

import sqlalchemy as sa
from alembic import op
from sqlalchemy.dialects import postgresql

revision = "0004"
down_revision = "0003"
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table(
        "place",
        sa.Column("id", sa.Text, primary_key=True),
        sa.Column("iso2", sa.Text, nullable=False),
        sa.Column("name", sa.Text, nullable=False),
        sa.Column("continent", sa.Text, nullable=False),
        sa.Column("geonames_id", sa.Integer, nullable=False),
        sa.Column("wikidata_id", sa.Text),
        sa.Column("run_id", postgresql.UUID(as_uuid=True), sa.ForeignKey("pipeline_run.id"), nullable=False),
    )

    each_statement = "for each statement execute function canary_refuse()"

    op.execute("create trigger place_no_delete before delete on place " + each_statement)  # SAFETY-GUARD
    op.execute("create trigger place_no_truncate before truncate on place " + each_statement)  # SAFETY-GUARD


def downgrade() -> None:
    raise NotImplementedError("0004 holds reference records; it is never undone by a migration")
