"""Tabela oportunidade COMPLETA (SPEC §2.3 + §3.2)

Cria oportunidade ja com todos os campos do SPEC §2.3 (sem fragmentar
em multiplas migrations). Inclui: 11 etapas (§3.2), 2 responsaveis,
temperaturas comercial/tecnica, scores tecnico/oportunidade, prazos,
cronograma, comite, OS, descarte/reativacao.

FK lead_id eh nullable: vendas direta nao tem lead pai.

Revision ID: 011
Revises: 010
Create Date: 2026-05-08
"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects.postgresql import UUID

revision: str = "011"
down_revision: Union[str, None] = "010"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.execute("CREATE SEQUENCE IF NOT EXISTS oportunidade_id_seq START 1")

    op.create_table(
        "oportunidade",
        sa.Column("id", UUID(as_uuid=True), primary_key=True, server_default=sa.text("gen_random_uuid()")),
        sa.Column("oportunidade_id", sa.String(10), nullable=False, unique=True),

        # FKs
        sa.Column("empresa_id", UUID(as_uuid=True), sa.ForeignKey("empresas.id"), nullable=False),
        sa.Column("lead_id", UUID(as_uuid=True), sa.ForeignKey("leads.id"), nullable=True),
        sa.Column("responsavel_comercial_id", UUID(as_uuid=True), sa.ForeignKey("users.id"), nullable=True),
        sa.Column("responsavel_tecnico_id", UUID(as_uuid=True), sa.ForeignKey("users.id"), nullable=True),
        sa.Column("area_atuacao_id", UUID(as_uuid=True), sa.ForeignKey("area_atuacao.id"), nullable=True),

        # Identificacao
        sa.Column("nome_projeto", sa.String(255), nullable=False),
        sa.Column("descricao_demanda", sa.Text),
        sa.Column("produto", sa.String(150)),
        sa.Column("tipo_entrega", sa.String(20)),

        # Etapa (11 valores - SPEC §3.2)
        sa.Column("etapa", sa.String(40), nullable=False, server_default="ESTIMATIVA"),

        # Lifecycle / handoff
        sa.Column("data_handoff", sa.DateTime),
        sa.Column("data_ultima_atividade", sa.DateTime),

        # Descarte / reativacao
        sa.Column("descartado", sa.Boolean, nullable=False, server_default=sa.text("false")),
        sa.Column("motivo_descarte", sa.Text),
        sa.Column("data_descarte", sa.DateTime),
        sa.Column("data_reativacao", sa.DateTime),
        sa.Column("status_reativacao", sa.String(50)),

        # Scores
        sa.Column("score_tecnico", sa.Numeric(5, 2)),
        sa.Column("score_oportunidade", sa.Numeric(5, 2)),

        # Temperatura
        sa.Column("temperatura_comercial", sa.String(10)),
        sa.Column("temperatura_tecnica", sa.String(10)),

        # Acao / forecast
        sa.Column("acao_recomendada", sa.String(255)),
        sa.Column("chance_conversao_pct", sa.Integer),
        sa.Column("data_prevista_venda", sa.Date),
        sa.Column("data_conclusao", sa.DateTime),

        # Aderencia / complexidade
        sa.Column("nivel_aderencia", sa.String(20)),
        sa.Column("nivel_complexidade", sa.String(20)),

        # Prazos / cronograma
        sa.Column("prazo_emissao_pedido", sa.Date),
        sa.Column("prazo_entrega_cliente", sa.Date),
        sa.Column("prazo_entrega_arv", sa.Date),
        sa.Column("cronograma_inicio", sa.Date),
        sa.Column("cronograma_fim", sa.Date),
        sa.Column("data_limite_aprovacao_comite", sa.Date),

        # Comite + visita
        sa.Column("passou_por_comite", sa.Boolean, nullable=False, server_default=sa.text("false")),
        sa.Column("visita_alinhamento_tecnico_necessaria", sa.Boolean, nullable=False, server_default=sa.text("false")),

        # Revisao / OS
        sa.Column("n_revisao", sa.Integer, nullable=False, server_default="1"),
        sa.Column("n_os", sa.String(20)),
        sa.Column("pasta_projeto_atualizada", sa.Boolean, nullable=False, server_default=sa.text("false")),

        # Lifecycle
        sa.Column("ativo", sa.Boolean, nullable=False, server_default=sa.text("true")),
        sa.Column("created_at", sa.DateTime, nullable=False, server_default=sa.func.now()),
        sa.Column("updated_at", sa.DateTime, nullable=False, server_default=sa.func.now()),

        # Constraints de enums (sem CREATE TYPE - usar CHECK pra simplicidade)
        sa.CheckConstraint(
            "etapa IN ('ESTIMATIVA', 'ESTIMATIVA_EM_CONVERSAO', 'PROJECAO_ORCAMENTARIA', "
            "'PROJECAO_EM_CONVERSAO', 'DESENVOLVIMENTO_PROPOSTA', 'PROPOSTA_ENVIADA', "
            "'PROPOSTA_EM_ANALISE_TECNICA', 'PROPOSTA_EM_ANALISE_COMERCIAL', "
            "'PROPOSTA_EM_NEGOCIACAO', 'EMISSAO_PEDIDO', 'CONVERTIDA_EM_VENDA')",
            name="ck_oportunidade_etapa",
        ),
        sa.CheckConstraint(
            "tipo_entrega IS NULL OR tipo_entrega IN ('estimativa', 'projecao', 'proposta')",
            name="ck_oportunidade_tipo_entrega",
        ),
        sa.CheckConstraint(
            "temperatura_comercial IS NULL OR temperatura_comercial IN ('frio', 'morno', 'quente')",
            name="ck_oportunidade_temp_comercial",
        ),
        sa.CheckConstraint(
            "temperatura_tecnica IS NULL OR temperatura_tecnica IN ('frio', 'morno', 'quente')",
            name="ck_oportunidade_temp_tecnica",
        ),
    )

    op.create_index("ix_oportunidade_empresa_id", "oportunidade", ["empresa_id"])
    op.create_index("ix_oportunidade_lead_id", "oportunidade", ["lead_id"])
    op.create_index("ix_oportunidade_responsavel_comercial_id", "oportunidade", ["responsavel_comercial_id"])
    op.create_index("ix_oportunidade_responsavel_tecnico_id", "oportunidade", ["responsavel_tecnico_id"])
    op.create_index("ix_oportunidade_etapa", "oportunidade", ["etapa"])
    op.create_index("ix_oportunidade_descartado", "oportunidade", ["descartado"])


def downgrade() -> None:
    op.drop_index("ix_oportunidade_descartado", "oportunidade")
    op.drop_index("ix_oportunidade_etapa", "oportunidade")
    op.drop_index("ix_oportunidade_responsavel_tecnico_id", "oportunidade")
    op.drop_index("ix_oportunidade_responsavel_comercial_id", "oportunidade")
    op.drop_index("ix_oportunidade_lead_id", "oportunidade")
    op.drop_index("ix_oportunidade_empresa_id", "oportunidade")
    op.drop_table("oportunidade")
    op.execute("DROP SEQUENCE IF EXISTS oportunidade_id_seq")
