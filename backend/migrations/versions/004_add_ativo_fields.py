"""Add ativo field to empresas and leads

Revision ID: 004
Revises: 003
Create Date: 2024-01-04
"""
from typing import Sequence, Union
from alembic import op
import sqlalchemy as sa

revision: str = "004"
down_revision: Union[str, None] = "003"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column("empresas", sa.Column("ativo", sa.Boolean, nullable=False, server_default=sa.text("true")))
    op.add_column("leads", sa.Column("ativo", sa.Boolean, nullable=False, server_default=sa.text("true")))


def downgrade() -> None:
    op.drop_column("leads", "ativo")
    op.drop_column("empresas", "ativo")
