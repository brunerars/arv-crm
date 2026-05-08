import uuid
from datetime import datetime, date

from sqlalchemy import String, Integer, Numeric, Boolean, DateTime, Date, ForeignKey, UniqueConstraint, func
import sqlalchemy as sa
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from database import Base


class Orcamento(Base):
    __tablename__ = "orcamento"
    __table_args__ = (
        UniqueConstraint("oportunidade_id", "versao", name="uq_orcamento_oportunidade_versao"),
    )

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    oportunidade_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), ForeignKey("oportunidade.id", ondelete="CASCADE"), nullable=False
    )
    versao: Mapped[int] = mapped_column(Integer, nullable=False)
    status_id: Mapped[uuid.UUID | None] = mapped_column(UUID(as_uuid=True), ForeignKey("status_orcamento.id"))

    valor_base: Mapped[float] = mapped_column(Numeric(15, 2), nullable=False, default=0, server_default="0")
    custo_fixo: Mapped[float] = mapped_column(Numeric(15, 2), nullable=False, default=0, server_default="0")
    custo_financeiro: Mapped[float] = mapped_column(Numeric(15, 2), nullable=False, default=0, server_default="0")
    custo_terceiros: Mapped[float] = mapped_column(Numeric(15, 2), nullable=False, default=0, server_default="0")
    custo_mao_obra: Mapped[float] = mapped_column(Numeric(15, 2), nullable=False, default=0, server_default="0")
    cmv_estimado: Mapped[float] = mapped_column(Numeric(15, 2), nullable=False, default=0, server_default="0")

    comissao_pct: Mapped[float] = mapped_column(Numeric(5, 2), nullable=False, default=0, server_default="0")
    markup_pct: Mapped[float] = mapped_column(Numeric(5, 2), nullable=False, default=0, server_default="0")

    ir_pct: Mapped[float] = mapped_column(Numeric(5, 2), nullable=False, default=0, server_default="0")
    csll_pct: Mapped[float] = mapped_column(Numeric(5, 2), nullable=False, default=0, server_default="0")
    icms_pct: Mapped[float] = mapped_column(Numeric(5, 2), nullable=False, default=0, server_default="0")
    iss_pct: Mapped[float] = mapped_column(Numeric(5, 2), nullable=False, default=0, server_default="0")
    pis_pct: Mapped[float] = mapped_column(Numeric(5, 2), nullable=False, default=0, server_default="0")
    cofins_pct: Mapped[float] = mapped_column(Numeric(5, 2), nullable=False, default=0, server_default="0")

    valor_com_imposto: Mapped[float | None] = mapped_column(Numeric(15, 2))
    valor_sem_imposto: Mapped[float | None] = mapped_column(Numeric(15, 2))

    antecipacao_prevista: Mapped[float | None] = mapped_column(Numeric(15, 2))
    antecipacao_confirmada: Mapped[float | None] = mapped_column(Numeric(15, 2))
    data_recebimento_antecipacao: Mapped[date | None] = mapped_column(Date)

    foi_enviado_cliente: Mapped[bool] = mapped_column(Boolean, nullable=False, default=False, server_default=sa.text("false"))
    data_envio: Mapped[datetime | None] = mapped_column(DateTime)
    cliente_confirmou_recebimento: Mapped[bool] = mapped_column(Boolean, nullable=False, default=False, server_default=sa.text("false"))
    prazo_avaliacao_tecnica_cliente: Mapped[date | None] = mapped_column(Date)
    solucao_tecnica_aprovada: Mapped[bool] = mapped_column(Boolean, nullable=False, default=False, server_default=sa.text("false"))
    prazo_analise_comercial_cliente: Mapped[date | None] = mapped_column(Date)
    email_enviado_comprador: Mapped[bool] = mapped_column(Boolean, nullable=False, default=False, server_default=sa.text("false"))
    condicoes_comerciais_aceitas: Mapped[bool] = mapped_column(Boolean, nullable=False, default=False, server_default=sa.text("false"))
    cliente_confirmou_intencao_compra: Mapped[bool] = mapped_column(Boolean, nullable=False, default=False, server_default=sa.text("false"))

    criado_por_id: Mapped[uuid.UUID | None] = mapped_column(UUID(as_uuid=True), ForeignKey("users.id"))
    created_at: Mapped[datetime] = mapped_column(DateTime, server_default=func.now())
    updated_at: Mapped[datetime] = mapped_column(DateTime, server_default=func.now(), onupdate=func.now())

    oportunidade = relationship("Oportunidade", foreign_keys=[oportunidade_id])
    status = relationship("StatusOrcamento", foreign_keys=[status_id])
    criado_por = relationship("User", foreign_keys=[criado_por_id])
