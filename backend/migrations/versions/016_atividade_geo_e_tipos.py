"""Atividade alignment com SPEC §7

- lead_id -> nullable; adiciona oportunidade_id, empresa_id, criada_por_id
- enum tipo (9 valores SPEC §7.1) via CHECK
- substitui concluida bool por status enum (planejada|em_andamento|
  realizada|cancelada)
- rename data_conclusao -> data_realizacao
- adiciona resultado, geo_uf, geo_cidade, geo_zona (SPEC §7.2)
- adiciona updated_at

Revision ID: 016
Revises: 015
Create Date: 2026-05-08
"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects.postgresql import UUID

revision: str = "016"
down_revision: Union[str, None] = "015"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.alter_column("atividades", "lead_id", nullable=True)

    op.add_column("atividades", sa.Column("oportunidade_id", UUID(as_uuid=True), sa.ForeignKey("oportunidade.id", ondelete="CASCADE"), nullable=True))
    op.add_column("atividades", sa.Column("empresa_id", UUID(as_uuid=True), sa.ForeignKey("empresas.id"), nullable=True))
    op.add_column("atividades", sa.Column("criada_por_id", UUID(as_uuid=True), sa.ForeignKey("users.id"), nullable=True))

    op.add_column("atividades", sa.Column("status", sa.String(20), nullable=False, server_default="planejada"))
    op.add_column("atividades", sa.Column("resultado", sa.Text))

    op.alter_column("atividades", "data_conclusao", new_column_name="data_realizacao")

    # Migra concluida -> status
    op.execute("UPDATE atividades SET status = 'realizada' WHERE concluida = TRUE")
    op.execute("UPDATE atividades SET status = 'planejada' WHERE concluida = FALSE")
    op.drop_column("atividades", "concluida")

    op.add_column("atividades", sa.Column("geo_uf", sa.String(2)))
    op.add_column("atividades", sa.Column("geo_cidade", sa.String(100)))
    op.add_column("atividades", sa.Column("geo_zona", sa.String(80)))
    op.add_column("atividades", sa.Column("updated_at", sa.DateTime, nullable=False, server_default=sa.func.now()))

    op.create_check_constraint(
        "ck_atividades_tipo",
        "atividades",
        "tipo IN ('email', 'ligacao', 'reuniao_interna', 'passagem_bastao', 'tarefa', "
        "'tarefa_tecnica', 'visita_comercial', 'visita_tecnica', 'apresentacao_proposta')",
    )
    op.create_check_constraint(
        "ck_atividades_status",
        "atividades",
        "status IN ('planejada', 'em_andamento', 'realizada', 'cancelada')",
    )
    op.create_check_constraint(
        "ck_atividades_target",
        "atividades",
        "lead_id IS NOT NULL OR oportunidade_id IS NOT NULL OR empresa_id IS NOT NULL",
    )

    op.create_index("ix_atividades_oportunidade_id", "atividades", ["oportunidade_id"])
    op.create_index("ix_atividades_empresa_id", "atividades", ["empresa_id"])
    op.create_index("ix_atividades_status", "atividades", ["status"])
    op.create_index("ix_atividades_data_prevista", "atividades", ["data_prevista"])


def downgrade() -> None:
    op.drop_index("ix_atividades_data_prevista", "atividades")
    op.drop_index("ix_atividades_status", "atividades")
    op.drop_index("ix_atividades_empresa_id", "atividades")
    op.drop_index("ix_atividades_oportunidade_id", "atividades")
    op.drop_constraint("ck_atividades_target", "atividades", type_="check")
    op.drop_constraint("ck_atividades_status", "atividades", type_="check")
    op.drop_constraint("ck_atividades_tipo", "atividades", type_="check")

    op.drop_column("atividades", "updated_at")
    op.drop_column("atividades", "geo_zona")
    op.drop_column("atividades", "geo_cidade")
    op.drop_column("atividades", "geo_uf")

    op.add_column("atividades", sa.Column("concluida", sa.Boolean, nullable=False, server_default=sa.text("false")))
    op.execute("UPDATE atividades SET concluida = TRUE WHERE status = 'realizada'")

    op.alter_column("atividades", "data_realizacao", new_column_name="data_conclusao")
    op.drop_column("atividades", "resultado")
    op.drop_column("atividades", "status")
    op.drop_column("atividades", "criada_por_id")
    op.drop_column("atividades", "empresa_id")
    op.drop_column("atividades", "oportunidade_id")

    op.execute("DELETE FROM atividades WHERE lead_id IS NULL")
    op.alter_column("atividades", "lead_id", nullable=False)
