"""Empresas, contatos, origens tables

Revision ID: 002
Revises: 001
Create Date: 2024-01-02
"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects.postgresql import UUID

revision: str = "002"
down_revision: Union[str, None] = "001"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        "empresas",
        sa.Column("id", UUID(as_uuid=True), primary_key=True, server_default=sa.text("gen_random_uuid()")),
        sa.Column("nome_fantasia", sa.String(255), nullable=False),
        sa.Column("razao_social", sa.String(255)),
        sa.Column("cnpj", sa.String(18), unique=True),
        sa.Column("segmento", sa.String(100)),
        sa.Column("num_funcionarios", sa.String(50)),
        sa.Column("num_plantas", sa.Integer),
        sa.Column("distancia_arv_km", sa.Numeric(10, 2)),
        sa.Column("cidade", sa.String(100)),
        sa.Column("estado", sa.String(2)),
        sa.Column("cep", sa.String(10)),
        sa.Column("telefone", sa.String(20)),
        sa.Column("site", sa.String(255)),
        sa.Column("status_conta", sa.String(30), nullable=False, server_default="prospect"),
        sa.Column("responsavel_id", UUID(as_uuid=True), sa.ForeignKey("users.id")),
        sa.Column("data_cadastro", sa.DateTime, nullable=False, server_default=sa.func.now()),
        sa.Column("observacoes", sa.Text),
        sa.Column("created_at", sa.DateTime, nullable=False, server_default=sa.func.now()),
        sa.Column("updated_at", sa.DateTime, nullable=False, server_default=sa.func.now()),
    )

    op.create_table(
        "contatos",
        sa.Column("id", UUID(as_uuid=True), primary_key=True, server_default=sa.text("gen_random_uuid()")),
        sa.Column("empresa_id", UUID(as_uuid=True), sa.ForeignKey("empresas.id", ondelete="CASCADE"), nullable=False),
        sa.Column("nome", sa.String(255), nullable=False),
        sa.Column("cargo", sa.String(100)),
        sa.Column("departamento", sa.String(100)),
        sa.Column("nivel_influencia", sa.String(20), server_default="operacional"),
        sa.Column("email", sa.String(255)),
        sa.Column("whatsapp", sa.String(20)),
        sa.Column("linkedin", sa.String(255)),
        sa.Column("ativo", sa.Boolean, nullable=False, server_default=sa.text("true")),
        sa.Column("data_cadastro", sa.DateTime, nullable=False, server_default=sa.func.now()),
        sa.Column("observacoes", sa.Text),
        sa.Column("created_at", sa.DateTime, nullable=False, server_default=sa.func.now()),
        sa.Column("updated_at", sa.DateTime, nullable=False, server_default=sa.func.now()),
    )

    op.create_table(
        "origens",
        sa.Column("id", UUID(as_uuid=True), primary_key=True, server_default=sa.text("gen_random_uuid()")),
        sa.Column("tipo", sa.String(20), nullable=False),
        sa.Column("sub_tipo", sa.String(30), nullable=False),
        sa.Column("descricao", sa.String(255)),
        sa.UniqueConstraint("tipo", "sub_tipo"),
    )

    # Seed origens
    op.execute("""
        INSERT INTO origens (id, tipo, sub_tipo, descricao) VALUES
        (gen_random_uuid(), 'passiva', 'site', 'Lead via site'),
        (gen_random_uuid(), 'passiva', 'indicacao_cliente', 'Indicação de cliente existente'),
        (gen_random_uuid(), 'passiva', 'indicacao_parceiro', 'Indicação de parceiro'),
        (gen_random_uuid(), 'ativa', 'pre_vendas', 'Prospecção ativa pré-vendas'),
        (gen_random_uuid(), 'ativa', 'vendas', 'Prospecção ativa vendas'),
        (gen_random_uuid(), 'ativa', 'linkedin', 'Prospecção via LinkedIn'),
        (gen_random_uuid(), 'indicacao', 'cliente', 'Indicação de cliente'),
        (gen_random_uuid(), 'indicacao', 'parceiro', 'Indicação de parceiro'),
        (gen_random_uuid(), 'indicacao', 'colaborador', 'Indicação de colaborador')
    """)


def downgrade() -> None:
    op.drop_table("origens")
    op.drop_table("contatos")
    op.drop_table("empresas")
