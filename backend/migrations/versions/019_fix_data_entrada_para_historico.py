"""Bugfix: substitui lead.data_entrada por consulta a historico_etapa_lead

SPEC v1.1 §12 + bug discovery: campo lead.data_entrada era usado como
"tempo na etapa atual" mas representava data de criacao do lead. Quando
lead muda de etapa, o tempo na etapa atual deve vir do registro mais
recente em historico_etapa_lead com saiu_em IS NULL.

DROP coluna data_entrada de leads (data_entrada_pre_vendas - adicionado
na 015 - cobre auditoria de quando entrou em pre-vendas; tempo na etapa
atual vai pra historico_etapa_lead.entrou_em).

Revision ID: 019
Revises: 018
Create Date: 2026-05-08
"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa

revision: str = "019"
down_revision: Union[str, None] = "018"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.drop_column("leads", "data_entrada")


def downgrade() -> None:
    op.add_column(
        "leads",
        sa.Column("data_entrada", sa.DateTime, nullable=False, server_default=sa.func.now()),
    )
    # Restaura valor a partir de data_entrada_pre_vendas (proxy razoavel)
    op.execute("UPDATE leads SET data_entrada = data_entrada_pre_vendas WHERE data_entrada IS NULL")
