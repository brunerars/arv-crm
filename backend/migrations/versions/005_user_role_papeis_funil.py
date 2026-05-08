"""User role enum (4 papeis funil) and ativo field

Revision ID: 005
Revises: 004
Create Date: 2026-05-08
"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa

revision: str = "005"
down_revision: Union[str, None] = "004"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column(
        "users",
        sa.Column("ativo", sa.Boolean, nullable=False, server_default=sa.text("true")),
    )

    # Migrate legacy 'user' role to 'vendas' (sensible default among the 4 papeis)
    op.execute("UPDATE users SET role = 'vendas' WHERE role NOT IN ('pre_vendas', 'vendas', 'tecnico', 'admin')")

    op.alter_column("users", "role", server_default="vendas")

    op.create_check_constraint(
        "ck_users_role",
        "users",
        "role IN ('pre_vendas', 'vendas', 'tecnico', 'admin')",
    )


def downgrade() -> None:
    op.drop_constraint("ck_users_role", "users", type_="check")
    op.alter_column("users", "role", server_default="user")
    op.drop_column("users", "ativo")
