"""Origem alignment com SPEC §7.3

Adiciona canal (3a dimensao livre: linkedin, site, indicacao, evento, cold_call,
feira, publicidade, etc) e relaxa sub_tipo (pode ser NULL quando tipo=PASSIVA).

Revision ID: 009
Revises: 008
Create Date: 2026-05-08
"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa

revision: str = "009"
down_revision: Union[str, None] = "008"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column("origens", sa.Column("canal", sa.String(50), nullable=True))
    op.alter_column("origens", "sub_tipo", nullable=True, existing_type=sa.String(30))


def downgrade() -> None:
    op.execute("UPDATE origens SET sub_tipo = 'sem_info' WHERE sub_tipo IS NULL")
    op.alter_column("origens", "sub_tipo", nullable=False, existing_type=sa.String(30))
    op.drop_column("origens", "canal")
