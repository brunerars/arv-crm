"""Leads, atividades, historico_etapas, scoring_respostas tables

Revision ID: 003
Revises: 002
Create Date: 2024-01-03
"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects.postgresql import UUID

revision: str = "003"
down_revision: Union[str, None] = "002"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # Sequence for lead_id
    op.execute("CREATE SEQUENCE IF NOT EXISTS lead_id_seq START 1")

    op.create_table(
        "leads",
        sa.Column("id", UUID(as_uuid=True), primary_key=True, server_default=sa.text("gen_random_uuid()")),
        sa.Column("lead_id", sa.String(10), nullable=False, unique=True),
        sa.Column("empresa_id", UUID(as_uuid=True), sa.ForeignKey("empresas.id"), nullable=False),
        sa.Column("contato_principal_id", UUID(as_uuid=True), sa.ForeignKey("contatos.id")),
        sa.Column("origem_id", UUID(as_uuid=True), sa.ForeignKey("origens.id")),
        sa.Column("responsavel_id", UUID(as_uuid=True), sa.ForeignKey("users.id")),
        sa.Column("etapa", sa.String(30), nullable=False, server_default="prospeccao"),
        sa.Column("sub_status", sa.String(50)),
        sa.Column("temperatura", sa.String(10), server_default="frio"),
        sa.Column("produto_interesse", sa.String(100)),
        sa.Column("area_atuacao", sa.String(100)),
        sa.Column("tipo_entrega", sa.String(50)),
        sa.Column("lead_score", sa.Integer, server_default="0"),
        sa.Column("classificacao", sa.String(30)),
        sa.Column("valor_estimado", sa.Numeric(15, 2), server_default="0"),
        sa.Column("motivo_descarte", sa.String(255)),
        sa.Column("data_entrada", sa.DateTime, nullable=False, server_default=sa.func.now()),
        sa.Column("data_qualificacao", sa.DateTime),
        sa.Column("prox_atividade", sa.String(100)),
        sa.Column("data_prox_atividade", sa.DateTime),
        sa.Column("created_at", sa.DateTime, nullable=False, server_default=sa.func.now()),
        sa.Column("updated_at", sa.DateTime, nullable=False, server_default=sa.func.now()),
    )

    op.create_table(
        "atividades",
        sa.Column("id", UUID(as_uuid=True), primary_key=True, server_default=sa.text("gen_random_uuid()")),
        sa.Column("lead_id", UUID(as_uuid=True), sa.ForeignKey("leads.id", ondelete="CASCADE"), nullable=False),
        sa.Column("responsavel_id", UUID(as_uuid=True), sa.ForeignKey("users.id")),
        sa.Column("tipo", sa.String(50), nullable=False),
        sa.Column("descricao", sa.Text),
        sa.Column("data_prevista", sa.DateTime),
        sa.Column("data_conclusao", sa.DateTime),
        sa.Column("concluida", sa.Boolean, nullable=False, server_default=sa.text("false")),
        sa.Column("created_at", sa.DateTime, nullable=False, server_default=sa.func.now()),
    )

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

    op.create_table(
        "scoring_respostas",
        sa.Column("id", UUID(as_uuid=True), primary_key=True, server_default=sa.text("gen_random_uuid()")),
        sa.Column("lead_id", UUID(as_uuid=True), sa.ForeignKey("leads.id", ondelete="CASCADE"), nullable=False),
        sa.Column("criterio", sa.String(50), nullable=False),
        sa.Column("valor", sa.String(100), nullable=False),
        sa.Column("pontos", sa.Integer, nullable=False),
        sa.Column("created_at", sa.DateTime, nullable=False, server_default=sa.func.now()),
    )


def downgrade() -> None:
    op.drop_table("scoring_respostas")
    op.drop_table("historico_etapas")
    op.drop_table("atividades")
    op.drop_table("leads")
    op.execute("DROP SEQUENCE IF EXISTS lead_id_seq")
