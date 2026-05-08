"""Tabela concorrente (SPEC §2.3)

Revision ID: 010
Revises: 009
Create Date: 2026-05-08
"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects.postgresql import UUID

revision: str = "010"
down_revision: Union[str, None] = "009"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        "concorrente",
        sa.Column("id", UUID(as_uuid=True), primary_key=True, server_default=sa.text("gen_random_uuid()")),
        sa.Column("cnpj", sa.String(18), unique=True),
        sa.Column("nome", sa.String(255), nullable=False),
        sa.Column("uf", sa.String(2)),
        sa.Column("cidade", sa.String(100)),
        sa.Column("qtde_filiais", sa.Integer),
        sa.Column("n_funcionarios_faixa", sa.String(50)),
        sa.Column("fundacao_ano", sa.Integer),
        sa.Column("portfolio", sa.Text),
        sa.Column("principais_clientes", sa.Text),
        sa.Column("principais_parceiros", sa.Text),
        sa.Column("observacoes", sa.Text),
        sa.Column("ativo", sa.Boolean, nullable=False, server_default=sa.text("true")),
        sa.Column("created_at", sa.DateTime, nullable=False, server_default=sa.func.now()),
        sa.Column("updated_at", sa.DateTime, nullable=False, server_default=sa.func.now()),
    )

    op.create_index("ix_concorrente_uf", "concorrente", ["uf"])
    op.create_index("ix_concorrente_ativo", "concorrente", ["ativo"])


def downgrade() -> None:
    op.drop_index("ix_concorrente_ativo", "concorrente")
    op.drop_index("ix_concorrente_uf", "concorrente")
    op.drop_table("concorrente")
