"""Tabela orcamento versionado (SPEC §2.3 + §1.3)

Cria orcamento como entidade propria com versionamento por oportunidade
(1 Oportunidade : N Orcamentos), impostos em % (NAO em R$ — corrige bug
do legado onde "Proposta sem Imposto" somava IR/CSLL erradamente),
custos detalhados e workflow de envio/aprovacao.

Revision ID: 012
Revises: 011
Create Date: 2026-05-08
"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects.postgresql import UUID

revision: str = "012"
down_revision: Union[str, None] = "011"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        "orcamento",
        sa.Column("id", UUID(as_uuid=True), primary_key=True, server_default=sa.text("gen_random_uuid()")),
        sa.Column("oportunidade_id", UUID(as_uuid=True), sa.ForeignKey("oportunidade.id", ondelete="CASCADE"), nullable=False),
        sa.Column("versao", sa.Integer, nullable=False),
        sa.Column("status_id", UUID(as_uuid=True), sa.ForeignKey("status_orcamento.id"), nullable=True),

        # Valor + custos
        sa.Column("valor_base", sa.Numeric(15, 2), nullable=False, server_default="0"),
        sa.Column("custo_fixo", sa.Numeric(15, 2), nullable=False, server_default="0"),
        sa.Column("custo_financeiro", sa.Numeric(15, 2), nullable=False, server_default="0"),
        sa.Column("custo_terceiros", sa.Numeric(15, 2), nullable=False, server_default="0"),
        sa.Column("custo_mao_obra", sa.Numeric(15, 2), nullable=False, server_default="0"),
        sa.Column("cmv_estimado", sa.Numeric(15, 2), nullable=False, server_default="0"),

        # Markups e comissao
        sa.Column("comissao_pct", sa.Numeric(5, 2), nullable=False, server_default="0"),
        sa.Column("markup_pct", sa.Numeric(5, 2), nullable=False, server_default="0"),

        # Impostos em % (corrige bug legado de impostos somados em R$)
        sa.Column("ir_pct", sa.Numeric(5, 2), nullable=False, server_default="0"),
        sa.Column("csll_pct", sa.Numeric(5, 2), nullable=False, server_default="0"),
        sa.Column("icms_pct", sa.Numeric(5, 2), nullable=False, server_default="0"),
        sa.Column("iss_pct", sa.Numeric(5, 2), nullable=False, server_default="0"),
        sa.Column("pis_pct", sa.Numeric(5, 2), nullable=False, server_default="0"),
        sa.Column("cofins_pct", sa.Numeric(5, 2), nullable=False, server_default="0"),

        # Valores calculados pelo app (NAO computed columns - mais simples manter app-controlled).
        # valor_sem_imposto = valor_base SEM somar IR/CSLL (eram bugs do legado).
        sa.Column("valor_com_imposto", sa.Numeric(15, 2)),
        sa.Column("valor_sem_imposto", sa.Numeric(15, 2)),

        # Antecipacoes
        sa.Column("antecipacao_prevista", sa.Numeric(15, 2)),
        sa.Column("antecipacao_confirmada", sa.Numeric(15, 2)),
        sa.Column("data_recebimento_antecipacao", sa.Date),

        # Workflow envio/aprovacao
        sa.Column("foi_enviado_cliente", sa.Boolean, nullable=False, server_default=sa.text("false")),
        sa.Column("data_envio", sa.DateTime),
        sa.Column("cliente_confirmou_recebimento", sa.Boolean, nullable=False, server_default=sa.text("false")),
        sa.Column("prazo_avaliacao_tecnica_cliente", sa.Date),
        sa.Column("solucao_tecnica_aprovada", sa.Boolean, nullable=False, server_default=sa.text("false")),
        sa.Column("prazo_analise_comercial_cliente", sa.Date),
        sa.Column("email_enviado_comprador", sa.Boolean, nullable=False, server_default=sa.text("false")),
        sa.Column("condicoes_comerciais_aceitas", sa.Boolean, nullable=False, server_default=sa.text("false")),
        sa.Column("cliente_confirmou_intencao_compra", sa.Boolean, nullable=False, server_default=sa.text("false")),

        # Audit
        sa.Column("criado_por_id", UUID(as_uuid=True), sa.ForeignKey("users.id"), nullable=True),
        sa.Column("created_at", sa.DateTime, nullable=False, server_default=sa.func.now()),
        sa.Column("updated_at", sa.DateTime, nullable=False, server_default=sa.func.now()),

        sa.UniqueConstraint("oportunidade_id", "versao", name="uq_orcamento_oportunidade_versao"),
    )

    op.create_index("ix_orcamento_oportunidade_id", "orcamento", ["oportunidade_id"])
    op.create_index("ix_orcamento_status_id", "orcamento", ["status_id"])


def downgrade() -> None:
    op.drop_index("ix_orcamento_status_id", "orcamento")
    op.drop_index("ix_orcamento_oportunidade_id", "orcamento")
    op.drop_table("orcamento")
