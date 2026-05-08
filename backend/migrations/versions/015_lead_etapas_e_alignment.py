"""Lead etapas (5 valores SPEC §3.1) + alignment

- Renames responsavel_id -> responsavel_pre_vendas_id
- Substitui enum etapa: prospeccao|primeiro_contato|qualificacao|qualificado|descartado
  -> LEAD_INICIAL|ANALISE_INTERNA|QUALIFICACAO_INICIAL|QUALIFICACAO_OPORTUNIDADE
  + flag descartado (SPEC §3.3 - descarte e flag, nao etapa terminal)
- Adiciona campos: nome_projeto, descricao_demanda, sub_origem_canal,
  data_ultima_atividade, data_entrada_pre_vendas, data_descarte,
  data_reativacao, status_reativacao, passou_por_comite

Revision ID: 015
Revises: 014
Create Date: 2026-05-08
"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa

revision: str = "015"
down_revision: Union[str, None] = "014"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.alter_column("leads", "responsavel_id", new_column_name="responsavel_pre_vendas_id")

    op.add_column("leads", sa.Column("descartado", sa.Boolean, nullable=False, server_default=sa.text("false")))
    op.add_column("leads", sa.Column("data_descarte", sa.DateTime))
    op.add_column("leads", sa.Column("data_reativacao", sa.DateTime))
    op.add_column("leads", sa.Column("status_reativacao", sa.String(50)))
    op.add_column("leads", sa.Column("nome_projeto", sa.String(255)))
    op.add_column("leads", sa.Column("descricao_demanda", sa.Text))
    op.add_column("leads", sa.Column("sub_origem_canal", sa.String(50)))
    op.add_column("leads", sa.Column("data_ultima_atividade", sa.DateTime))
    op.add_column("leads", sa.Column("data_entrada_pre_vendas", sa.DateTime, server_default=sa.func.now()))
    op.add_column("leads", sa.Column("passou_por_comite", sa.Boolean, nullable=False, server_default=sa.text("false")))

    # Mapeia descarte (etapa antiga 'descartado' -> flag descartado=true)
    op.execute("UPDATE leads SET descartado = TRUE, data_descarte = updated_at WHERE etapa = 'descartado'")

    # Mapeia etapas antigas -> novas
    op.execute("UPDATE leads SET etapa = 'LEAD_INICIAL' WHERE etapa IN ('prospeccao', 'descartado')")
    op.execute("UPDATE leads SET etapa = 'ANALISE_INTERNA' WHERE etapa = 'primeiro_contato'")
    op.execute("UPDATE leads SET etapa = 'QUALIFICACAO_INICIAL' WHERE etapa = 'qualificacao'")
    op.execute("UPDATE leads SET etapa = 'QUALIFICACAO_OPORTUNIDADE' WHERE etapa = 'qualificado'")

    op.execute("UPDATE leads SET data_entrada_pre_vendas = data_entrada")
    op.alter_column("leads", "data_entrada_pre_vendas", nullable=False)

    op.alter_column("leads", "etapa", server_default="LEAD_INICIAL")

    op.create_check_constraint(
        "ck_leads_etapa",
        "leads",
        "etapa IN ('LEAD_INICIAL', 'ANALISE_INTERNA', 'QUALIFICACAO_INICIAL', 'QUALIFICACAO_OPORTUNIDADE')",
    )

    op.create_index("ix_leads_descartado", "leads", ["descartado"])
    op.create_index("ix_leads_etapa_new", "leads", ["etapa"])


def downgrade() -> None:
    op.drop_index("ix_leads_etapa_new", "leads")
    op.drop_index("ix_leads_descartado", "leads")
    op.drop_constraint("ck_leads_etapa", "leads", type_="check")
    op.alter_column("leads", "etapa", server_default="prospeccao")

    op.execute("UPDATE leads SET etapa = 'qualificado' WHERE etapa = 'QUALIFICACAO_OPORTUNIDADE'")
    op.execute("UPDATE leads SET etapa = 'qualificacao' WHERE etapa = 'QUALIFICACAO_INICIAL'")
    op.execute("UPDATE leads SET etapa = 'primeiro_contato' WHERE etapa = 'ANALISE_INTERNA'")
    op.execute("UPDATE leads SET etapa = 'prospeccao' WHERE etapa = 'LEAD_INICIAL' AND descartado = FALSE")
    op.execute("UPDATE leads SET etapa = 'descartado' WHERE descartado = TRUE")

    op.drop_column("leads", "passou_por_comite")
    op.drop_column("leads", "data_entrada_pre_vendas")
    op.drop_column("leads", "data_ultima_atividade")
    op.drop_column("leads", "sub_origem_canal")
    op.drop_column("leads", "descricao_demanda")
    op.drop_column("leads", "nome_projeto")
    op.drop_column("leads", "status_reativacao")
    op.drop_column("leads", "data_reativacao")
    op.drop_column("leads", "data_descarte")
    op.drop_column("leads", "descartado")

    op.alter_column("leads", "responsavel_pre_vendas_id", new_column_name="responsavel_id")
