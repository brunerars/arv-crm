"""ScoringResposta alignment com SPEC §2.3 + §5

- lead_id -> nullable
- adiciona oportunidade_id (FK), categoria (TECNICO|OPORTUNIDADE),
  pergunta_codigo, opcao_codigo, valor_pontos, respondido_em,
  respondido_por_id
- mantem criterio/valor/pontos legacy (scoring_service atual usa);
  Macro B refatora service e dropa legacy

Revision ID: 017
Revises: 016
Create Date: 2026-05-08
"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects.postgresql import UUID

revision: str = "017"
down_revision: Union[str, None] = "016"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.alter_column("scoring_respostas", "lead_id", nullable=True)

    op.add_column("scoring_respostas", sa.Column("oportunidade_id", UUID(as_uuid=True), sa.ForeignKey("oportunidade.id", ondelete="CASCADE"), nullable=True))
    op.add_column("scoring_respostas", sa.Column("categoria", sa.String(20), nullable=False, server_default="TECNICO"))
    op.add_column("scoring_respostas", sa.Column("pergunta_codigo", sa.String(80)))
    op.add_column("scoring_respostas", sa.Column("opcao_codigo", sa.String(80)))
    op.add_column("scoring_respostas", sa.Column("valor_pontos", sa.Numeric(6, 2)))
    op.add_column("scoring_respostas", sa.Column("respondido_em", sa.DateTime))
    op.add_column("scoring_respostas", sa.Column("respondido_por_id", UUID(as_uuid=True), sa.ForeignKey("users.id"), nullable=True))

    # Migra valores legacy para campos novos (mantem ambos populados durante transicao)
    op.execute(
        "UPDATE scoring_respostas SET "
        "pergunta_codigo = criterio, "
        "opcao_codigo = valor, "
        "valor_pontos = pontos, "
        "respondido_em = created_at "
        "WHERE pergunta_codigo IS NULL"
    )

    op.create_check_constraint(
        "ck_scoring_respostas_categoria",
        "scoring_respostas",
        "categoria IN ('TECNICO', 'OPORTUNIDADE')",
    )
    op.create_check_constraint(
        "ck_scoring_respostas_target",
        "scoring_respostas",
        "lead_id IS NOT NULL OR oportunidade_id IS NOT NULL",
    )

    op.create_index("ix_scoring_respostas_oportunidade_id", "scoring_respostas", ["oportunidade_id"])
    op.create_index("ix_scoring_respostas_categoria", "scoring_respostas", ["categoria"])
    op.create_index("ix_scoring_respostas_pergunta", "scoring_respostas", ["pergunta_codigo"])


def downgrade() -> None:
    op.drop_index("ix_scoring_respostas_pergunta", "scoring_respostas")
    op.drop_index("ix_scoring_respostas_categoria", "scoring_respostas")
    op.drop_index("ix_scoring_respostas_oportunidade_id", "scoring_respostas")
    op.drop_constraint("ck_scoring_respostas_target", "scoring_respostas", type_="check")
    op.drop_constraint("ck_scoring_respostas_categoria", "scoring_respostas", type_="check")

    op.drop_column("scoring_respostas", "respondido_por_id")
    op.drop_column("scoring_respostas", "respondido_em")
    op.drop_column("scoring_respostas", "valor_pontos")
    op.drop_column("scoring_respostas", "opcao_codigo")
    op.drop_column("scoring_respostas", "pergunta_codigo")
    op.drop_column("scoring_respostas", "categoria")
    op.drop_column("scoring_respostas", "oportunidade_id")

    op.execute("DELETE FROM scoring_respostas WHERE lead_id IS NULL")
    op.alter_column("scoring_respostas", "lead_id", nullable=False)
