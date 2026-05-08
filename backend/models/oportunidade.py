import uuid
from datetime import datetime, date
from decimal import Decimal

from sqlalchemy import String, Integer, Numeric, Boolean, DateTime, Date, Text, ForeignKey, Sequence, func
import sqlalchemy as sa
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from database import Base

oportunidade_id_seq = Sequence("oportunidade_id_seq")

ETAPAS_OPORTUNIDADE = (
    "ESTIMATIVA",
    "ESTIMATIVA_EM_CONVERSAO",
    "PROJECAO_ORCAMENTARIA",
    "PROJECAO_EM_CONVERSAO",
    "DESENVOLVIMENTO_PROPOSTA",
    "PROPOSTA_ENVIADA",
    "PROPOSTA_EM_ANALISE_TECNICA",
    "PROPOSTA_EM_ANALISE_COMERCIAL",
    "PROPOSTA_EM_NEGOCIACAO",
    "EMISSAO_PEDIDO",
    "CONVERTIDA_EM_VENDA",
)

TIPOS_ENTREGA = ("estimativa", "projecao", "proposta")
TEMPERATURAS = ("frio", "morno", "quente")


class Oportunidade(Base):
    __tablename__ = "oportunidade"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    oportunidade_id: Mapped[str] = mapped_column(String(10), unique=True, nullable=False)

    empresa_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), ForeignKey("empresas.id"), nullable=False)
    lead_id: Mapped[uuid.UUID | None] = mapped_column(UUID(as_uuid=True), ForeignKey("leads.id"))
    responsavel_comercial_id: Mapped[uuid.UUID | None] = mapped_column(UUID(as_uuid=True), ForeignKey("users.id"))
    responsavel_tecnico_id: Mapped[uuid.UUID | None] = mapped_column(UUID(as_uuid=True), ForeignKey("users.id"))
    area_atuacao_id: Mapped[uuid.UUID | None] = mapped_column(UUID(as_uuid=True), ForeignKey("area_atuacao.id"))

    nome_projeto: Mapped[str] = mapped_column(String(255), nullable=False)
    descricao_demanda: Mapped[str | None] = mapped_column(Text)
    produto: Mapped[str | None] = mapped_column(String(150))
    tipo_entrega: Mapped[str | None] = mapped_column(String(20))

    etapa: Mapped[str] = mapped_column(String(40), nullable=False, default="ESTIMATIVA", server_default="ESTIMATIVA")

    data_handoff: Mapped[datetime | None] = mapped_column(DateTime)
    data_ultima_atividade: Mapped[datetime | None] = mapped_column(DateTime)

    descartado: Mapped[bool] = mapped_column(Boolean, nullable=False, default=False, server_default=sa.text("false"))
    motivo_descarte: Mapped[str | None] = mapped_column(Text)
    data_descarte: Mapped[datetime | None] = mapped_column(DateTime)
    data_reativacao: Mapped[datetime | None] = mapped_column(DateTime)
    status_reativacao: Mapped[str | None] = mapped_column(String(50))

    score_tecnico: Mapped[float | None] = mapped_column(Numeric(5, 2))
    score_oportunidade: Mapped[float | None] = mapped_column(Numeric(5, 2))
    temperatura_comercial: Mapped[str | None] = mapped_column(String(10))
    temperatura_tecnica: Mapped[str | None] = mapped_column(String(10))

    acao_recomendada: Mapped[str | None] = mapped_column(String(255))
    chance_conversao_pct: Mapped[int | None] = mapped_column(Integer)
    data_prevista_venda: Mapped[date | None] = mapped_column(Date)
    data_conclusao: Mapped[datetime | None] = mapped_column(DateTime)

    nivel_aderencia: Mapped[str | None] = mapped_column(String(20))
    nivel_complexidade: Mapped[str | None] = mapped_column(String(20))

    prazo_emissao_pedido: Mapped[date | None] = mapped_column(Date)
    prazo_entrega_cliente: Mapped[date | None] = mapped_column(Date)
    prazo_entrega_arv: Mapped[date | None] = mapped_column(Date)
    cronograma_inicio: Mapped[date | None] = mapped_column(Date)
    cronograma_fim: Mapped[date | None] = mapped_column(Date)
    data_limite_aprovacao_comite: Mapped[date | None] = mapped_column(Date)

    passou_por_comite: Mapped[bool] = mapped_column(Boolean, nullable=False, default=False, server_default=sa.text("false"))
    visita_alinhamento_tecnico_necessaria: Mapped[bool] = mapped_column(Boolean, nullable=False, default=False, server_default=sa.text("false"))

    n_revisao: Mapped[int] = mapped_column(Integer, nullable=False, default=1, server_default="1")
    n_os: Mapped[str | None] = mapped_column(String(20))
    pasta_projeto_atualizada: Mapped[bool] = mapped_column(Boolean, nullable=False, default=False, server_default=sa.text("false"))

    ativo: Mapped[bool] = mapped_column(Boolean, nullable=False, default=True, server_default=sa.text("true"))
    created_at: Mapped[datetime] = mapped_column(DateTime, server_default=func.now())
    updated_at: Mapped[datetime] = mapped_column(DateTime, server_default=func.now(), onupdate=func.now())

    empresa = relationship("Empresa", foreign_keys=[empresa_id])
    lead = relationship("Lead", foreign_keys=[lead_id])
    responsavel_comercial = relationship("User", foreign_keys=[responsavel_comercial_id])
    responsavel_tecnico = relationship("User", foreign_keys=[responsavel_tecnico_id])
    area_atuacao = relationship("AreaAtuacao", foreign_keys=[area_atuacao_id])
