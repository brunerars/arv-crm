"""Tabela meta_vendas (SPEC §2.3)

Substitui meta hardcoded em formula Monday. Suporta escopo
GLOBAL, USER, ETAPA, ETAPA_USER com pelo menos quantidade_meta
ou valor_meta preenchido.

Revision ID: 013
Revises: 012
Create Date: 2026-05-08
"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects.postgresql import UUID

revision: str = "013"
down_revision: Union[str, None] = "012"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        "meta_vendas",
        sa.Column("id", UUID(as_uuid=True), primary_key=True, server_default=sa.text("gen_random_uuid()")),
        sa.Column("periodo_inicio", sa.Date, nullable=False),
        sa.Column("periodo_fim", sa.Date, nullable=False),
        sa.Column("escopo", sa.String(20), nullable=False),
        sa.Column("user_id", UUID(as_uuid=True), sa.ForeignKey("users.id"), nullable=True),
        sa.Column("etapa", sa.String(40), nullable=True),
        sa.Column("quantidade_meta", sa.Integer, nullable=True),
        sa.Column("valor_meta", sa.Numeric(15, 2), nullable=True),
        sa.Column("created_at", sa.DateTime, nullable=False, server_default=sa.func.now()),
        sa.Column("updated_at", sa.DateTime, nullable=False, server_default=sa.func.now()),

        sa.CheckConstraint(
            "escopo IN ('GLOBAL', 'USER', 'ETAPA', 'ETAPA_USER')",
            name="ck_meta_vendas_escopo",
        ),
        sa.CheckConstraint(
            "(escopo = 'GLOBAL' AND user_id IS NULL AND etapa IS NULL) OR "
            "(escopo = 'USER' AND user_id IS NOT NULL AND etapa IS NULL) OR "
            "(escopo = 'ETAPA' AND user_id IS NULL AND etapa IS NOT NULL) OR "
            "(escopo = 'ETAPA_USER' AND user_id IS NOT NULL AND etapa IS NOT NULL)",
            name="ck_meta_vendas_escopo_consistency",
        ),
        sa.CheckConstraint(
            "quantidade_meta IS NOT NULL OR valor_meta IS NOT NULL",
            name="ck_meta_vendas_pelo_menos_um_valor",
        ),
        sa.CheckConstraint(
            "periodo_fim >= periodo_inicio",
            name="ck_meta_vendas_periodo_valido",
        ),
    )

    op.create_index("ix_meta_vendas_periodo", "meta_vendas", ["periodo_inicio", "periodo_fim"])
    op.create_index("ix_meta_vendas_user_id", "meta_vendas", ["user_id"])
    op.create_index("ix_meta_vendas_escopo", "meta_vendas", ["escopo"])


def downgrade() -> None:
    op.drop_index("ix_meta_vendas_escopo", "meta_vendas")
    op.drop_index("ix_meta_vendas_user_id", "meta_vendas")
    op.drop_index("ix_meta_vendas_periodo", "meta_vendas")
    op.drop_table("meta_vendas")
