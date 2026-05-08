"""Historico de etapas split: DROP historico_etapas + CREATE 2 tabelas

Em dev (sem prod, sem dados reais valiosos), DROP + CREATE eh correto
ao inves de migracao de dados, ja que schema antigo (etapa_anterior,
etapa_nova, tempo_na_etapa_segundos) e estruturalmente incompativel
com SPEC §3 (etapa, entrou_em, saiu_em, responsavel_no_periodo_id).

Cria 2 tabelas separadas (SPEC §3 + §1.1):
- historico_etapa_lead: para Lead (5 etapas pre-vendas)
- historico_etapa_oportunidade: para Oportunidade (8/11 etapas vendas)

Indice parcial em saiu_em IS NULL acelera consulta de "etapa atual"
(usado por SPEC §6 SLA + dashboards).

Revision ID: 018
Revises: 017
Create Date: 2026-05-08
"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects.postgresql import UUID

revision: str = "018"
down_revision: Union[str, None] = "017"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.drop_table("historico_etapas")

    op.create_table(
        "historico_etapa_lead",
        sa.Column("id", UUID(as_uuid=True), primary_key=True, server_default=sa.text("gen_random_uuid()")),
        sa.Column("lead_id", UUID(as_uuid=True), sa.ForeignKey("leads.id", ondelete="CASCADE"), nullable=False),
        sa.Column("etapa", sa.String(40), nullable=False),
        sa.Column("entrou_em", sa.DateTime, nullable=False, server_default=sa.func.now()),
        sa.Column("saiu_em", sa.DateTime, nullable=True),
        sa.Column("responsavel_no_periodo_id", UUID(as_uuid=True), sa.ForeignKey("users.id"), nullable=True),
    )
    op.create_index("ix_historico_etapa_lead_lead_id", "historico_etapa_lead", ["lead_id"])
    op.create_index("ix_historico_etapa_lead_etapa", "historico_etapa_lead", ["etapa"])
    op.create_index(
        "ix_historico_etapa_lead_atual",
        "historico_etapa_lead",
        ["lead_id"],
        postgresql_where=sa.text("saiu_em IS NULL"),
    )

    op.create_table(
        "historico_etapa_oportunidade",
        sa.Column("id", UUID(as_uuid=True), primary_key=True, server_default=sa.text("gen_random_uuid()")),
        sa.Column("oportunidade_id", UUID(as_uuid=True), sa.ForeignKey("oportunidade.id", ondelete="CASCADE"), nullable=False),
        sa.Column("etapa", sa.String(40), nullable=False),
        sa.Column("entrou_em", sa.DateTime, nullable=False, server_default=sa.func.now()),
        sa.Column("saiu_em", sa.DateTime, nullable=True),
        sa.Column("responsavel_no_periodo_id", UUID(as_uuid=True), sa.ForeignKey("users.id"), nullable=True),
    )
    op.create_index("ix_historico_etapa_opp_opp_id", "historico_etapa_oportunidade", ["oportunidade_id"])
    op.create_index("ix_historico_etapa_opp_etapa", "historico_etapa_oportunidade", ["etapa"])
    op.create_index(
        "ix_historico_etapa_opp_atual",
        "historico_etapa_oportunidade",
        ["oportunidade_id"],
        postgresql_where=sa.text("saiu_em IS NULL"),
    )


def downgrade() -> None:
    op.drop_index("ix_historico_etapa_opp_atual", "historico_etapa_oportunidade")
    op.drop_index("ix_historico_etapa_opp_etapa", "historico_etapa_oportunidade")
    op.drop_index("ix_historico_etapa_opp_opp_id", "historico_etapa_oportunidade")
    op.drop_table("historico_etapa_oportunidade")

    op.drop_index("ix_historico_etapa_lead_atual", "historico_etapa_lead")
    op.drop_index("ix_historico_etapa_lead_etapa", "historico_etapa_lead")
    op.drop_index("ix_historico_etapa_lead_lead_id", "historico_etapa_lead")
    op.drop_table("historico_etapa_lead")

    op.create_table(
        "historico_etapas",
        sa.Column("id", UUID(as_uuid=True), primary_key=True, server_default=sa.text("gen_random_uuid()")),
        sa.Column("lead_id", UUID(as_uuid=True), sa.ForeignKey("leads.id", ondelete="CASCADE"), nullable=False),
        sa.Column("etapa_anterior", sa.String(30)),
        sa.Column("etapa_nova", sa.String(30), nullable=False),
        sa.Column("tempo_na_etapa_segundos", sa.Integer),
        sa.Column("usuario_id", UUID(as_uuid=True), sa.ForeignKey("users.id")),
        sa.Column("created_at", sa.DateTime, nullable=False, server_default=sa.func.now()),
    )
