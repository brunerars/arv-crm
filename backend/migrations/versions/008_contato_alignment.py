"""Contato alignment com SPEC §2.3

Novos valores de nivel_influencia (decisor|influenciador|usuario|tecnico|sem_info)
+ rename whatsapp -> telefone_whatsapp + adiciona papel_decisao.

Revision ID: 008
Revises: 007
Create Date: 2026-05-08
"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa

revision: str = "008"
down_revision: Union[str, None] = "007"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.alter_column("contatos", "whatsapp", new_column_name="telefone_whatsapp")

    op.execute("UPDATE contatos SET nivel_influencia = 'usuario' WHERE nivel_influencia = 'operacional'")
    op.execute(
        "UPDATE contatos SET nivel_influencia = 'sem_info' "
        "WHERE nivel_influencia IS NULL OR nivel_influencia NOT IN "
        "('decisor', 'influenciador', 'usuario', 'tecnico', 'sem_info')"
    )

    op.alter_column(
        "contatos",
        "nivel_influencia",
        server_default="sem_info",
        nullable=False,
        existing_type=sa.String(20),
    )

    op.create_check_constraint(
        "ck_contatos_nivel_influencia",
        "contatos",
        "nivel_influencia IN ('decisor', 'influenciador', 'usuario', 'tecnico', 'sem_info')",
    )

    op.add_column("contatos", sa.Column("papel_decisao", sa.Text, nullable=True))


def downgrade() -> None:
    op.drop_column("contatos", "papel_decisao")
    op.drop_constraint("ck_contatos_nivel_influencia", "contatos", type_="check")
    op.alter_column(
        "contatos",
        "nivel_influencia",
        server_default="operacional",
        existing_type=sa.String(20),
    )
    op.execute(
        "UPDATE contatos SET nivel_influencia = 'operacional' "
        "WHERE nivel_influencia IN ('usuario', 'tecnico', 'sem_info')"
    )
    op.alter_column("contatos", "telefone_whatsapp", new_column_name="whatsapp")
