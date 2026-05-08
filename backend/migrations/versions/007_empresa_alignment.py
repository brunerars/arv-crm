"""Empresa alignment com SPEC §2.3

Renames + drops de campos string que viram FKs para tabelas de referencia +
adiciona ICP fields (score, classificacao) + tipo (FK) + is_cliente.

Revision ID: 007
Revises: 006
Create Date: 2026-05-08
"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects.postgresql import UUID

revision: str = "007"
down_revision: Union[str, None] = "006"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.alter_column("empresas", "num_plantas", new_column_name="n_plantas_industriais")
    op.alter_column("empresas", "distancia_arv_km", new_column_name="distancia_planta_km")
    op.alter_column("empresas", "estado", new_column_name="estado_uf")
    op.alter_column("empresas", "telefone", new_column_name="telefone_fixo")

    # Drop campos que viram FK ou tipo melhor.
    # Em dev (sem prod), valores ficam perdidos. Quando seed rodar (script
    # seed_referencias.py), FKs sao populados via mapping nome→FK.
    op.drop_column("empresas", "segmento")
    op.drop_column("empresas", "num_funcionarios")
    op.drop_column("empresas", "data_cadastro")  # redundante com created_at

    op.add_column("empresas", sa.Column("segmento_mercado_id", UUID(as_uuid=True), sa.ForeignKey("segmento_mercado.id"), nullable=True))
    op.add_column("empresas", sa.Column("area_atuacao_id", UUID(as_uuid=True), sa.ForeignKey("area_atuacao.id"), nullable=True))
    op.add_column("empresas", sa.Column("tipo_id", UUID(as_uuid=True), sa.ForeignKey("tipo_empresa.id"), nullable=True))

    op.add_column("empresas", sa.Column("quantidade_funcionarios", sa.Integer, nullable=True))
    op.add_column("empresas", sa.Column("tempo_mercado_anos", sa.Integer, nullable=True))
    op.add_column("empresas", sa.Column("endereco_numero", sa.String(20), nullable=True))
    op.add_column("empresas", sa.Column("endereco_complemento", sa.String(100), nullable=True))
    op.add_column("empresas", sa.Column("linkedin", sa.String(255), nullable=True))
    op.add_column("empresas", sa.Column("is_cliente", sa.Boolean, nullable=False, server_default=sa.text("false")))
    op.add_column("empresas", sa.Column("icp_score", sa.Numeric(5, 2), nullable=True))
    op.add_column("empresas", sa.Column("icp_classificacao", sa.String(1), nullable=True))

    # Migrar status_conta='cliente_ativo' -> is_cliente=true antes de dropar
    op.execute("UPDATE empresas SET is_cliente = TRUE WHERE status_conta = 'cliente_ativo'")
    op.drop_column("empresas", "status_conta")

    op.create_check_constraint(
        "ck_empresas_icp_classificacao",
        "empresas",
        "icp_classificacao IS NULL OR icp_classificacao IN ('A', 'B', 'C')",
    )

    op.create_index("ix_empresas_segmento_mercado_id", "empresas", ["segmento_mercado_id"])
    op.create_index("ix_empresas_tipo_id", "empresas", ["tipo_id"])
    op.create_index("ix_empresas_is_cliente", "empresas", ["is_cliente"])


def downgrade() -> None:
    op.drop_index("ix_empresas_is_cliente", "empresas")
    op.drop_index("ix_empresas_tipo_id", "empresas")
    op.drop_index("ix_empresas_segmento_mercado_id", "empresas")
    op.drop_constraint("ck_empresas_icp_classificacao", "empresas", type_="check")

    op.add_column("empresas", sa.Column("status_conta", sa.String(30), nullable=False, server_default="prospect"))
    op.execute("UPDATE empresas SET status_conta = 'cliente_ativo' WHERE is_cliente = TRUE")

    op.drop_column("empresas", "icp_classificacao")
    op.drop_column("empresas", "icp_score")
    op.drop_column("empresas", "is_cliente")
    op.drop_column("empresas", "linkedin")
    op.drop_column("empresas", "endereco_complemento")
    op.drop_column("empresas", "endereco_numero")
    op.drop_column("empresas", "tempo_mercado_anos")
    op.drop_column("empresas", "quantidade_funcionarios")
    op.drop_column("empresas", "tipo_id")
    op.drop_column("empresas", "area_atuacao_id")
    op.drop_column("empresas", "segmento_mercado_id")

    op.add_column("empresas", sa.Column("data_cadastro", sa.DateTime, nullable=False, server_default=sa.func.now()))
    op.add_column("empresas", sa.Column("num_funcionarios", sa.String(50), nullable=True))
    op.add_column("empresas", sa.Column("segmento", sa.String(100), nullable=True))

    op.alter_column("empresas", "telefone_fixo", new_column_name="telefone")
    op.alter_column("empresas", "estado_uf", new_column_name="estado")
    op.alter_column("empresas", "distancia_planta_km", new_column_name="distancia_arv_km")
    op.alter_column("empresas", "n_plantas_industriais", new_column_name="num_plantas")
