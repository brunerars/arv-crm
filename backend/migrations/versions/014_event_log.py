"""Tabela event_log (SPEC §9)

Rastreabilidade de eventos webhook (saida + entrada). Schema preparado
para retry com APScheduler (Macro E1): attempts, last_error,
delivered_at, indice parcial em undelivered.

Revision ID: 014
Revises: 013
Create Date: 2026-05-08
"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects.postgresql import UUID, JSONB

revision: str = "014"
down_revision: Union[str, None] = "013"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        "event_log",
        sa.Column("id", UUID(as_uuid=True), primary_key=True, server_default=sa.text("gen_random_uuid()")),
        sa.Column("event", sa.String(80), nullable=False),
        sa.Column("version", sa.String(10), nullable=False, server_default="1.0"),
        sa.Column("direction", sa.String(10), nullable=False),
        sa.Column("payload", JSONB, nullable=False),
        sa.Column("occurred_at", sa.DateTime, nullable=False, server_default=sa.func.now()),
        sa.Column("delivered_at", sa.DateTime),
        sa.Column("attempts", sa.Integer, nullable=False, server_default="0"),
        sa.Column("last_error", sa.Text),
        sa.Column("target_url", sa.String(500)),
        sa.Column("source", sa.String(80)),
        sa.Column("created_at", sa.DateTime, nullable=False, server_default=sa.func.now()),

        sa.CheckConstraint("direction IN ('saida', 'entrada')", name="ck_event_log_direction"),
    )

    op.create_index("ix_event_log_event", "event_log", ["event"])
    op.create_index("ix_event_log_direction", "event_log", ["direction"])
    op.create_index("ix_event_log_occurred_at", "event_log", ["occurred_at"])
    op.create_index(
        "ix_event_log_undelivered",
        "event_log",
        ["occurred_at"],
        postgresql_where=sa.text("delivered_at IS NULL AND direction = 'saida'"),
    )


def downgrade() -> None:
    op.drop_index("ix_event_log_undelivered", "event_log")
    op.drop_index("ix_event_log_occurred_at", "event_log")
    op.drop_index("ix_event_log_direction", "event_log")
    op.drop_index("ix_event_log_event", "event_log")
    op.drop_table("event_log")
