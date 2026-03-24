import uuid
from datetime import datetime

from sqlalchemy import String, Integer, Numeric, Boolean, DateTime, Text, ForeignKey, Sequence, func
import sqlalchemy as sa
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from database import Base

lead_id_seq = Sequence("lead_id_seq")


class Lead(Base):
    __tablename__ = "leads"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    lead_id: Mapped[str] = mapped_column(String(10), unique=True, nullable=False)
    empresa_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), ForeignKey("empresas.id"), nullable=False)
    contato_principal_id: Mapped[uuid.UUID | None] = mapped_column(UUID(as_uuid=True), ForeignKey("contatos.id"))
    origem_id: Mapped[uuid.UUID | None] = mapped_column(UUID(as_uuid=True), ForeignKey("origens.id"))
    responsavel_id: Mapped[uuid.UUID | None] = mapped_column(UUID(as_uuid=True), ForeignKey("users.id"))
    etapa: Mapped[str] = mapped_column(String(30), nullable=False, default="prospeccao")
    sub_status: Mapped[str | None] = mapped_column(String(50))
    temperatura: Mapped[str] = mapped_column(String(10), default="frio")
    produto_interesse: Mapped[str | None] = mapped_column(String(100))
    area_atuacao: Mapped[str | None] = mapped_column(String(100))
    tipo_entrega: Mapped[str | None] = mapped_column(String(50))
    lead_score: Mapped[int] = mapped_column(Integer, default=0)
    classificacao: Mapped[str | None] = mapped_column(String(30))
    valor_estimado: Mapped[float] = mapped_column(Numeric(15, 2), default=0)
    motivo_descarte: Mapped[str | None] = mapped_column(String(255))
    data_entrada: Mapped[datetime] = mapped_column(DateTime, server_default=func.now())
    data_qualificacao: Mapped[datetime | None] = mapped_column(DateTime)
    prox_atividade: Mapped[str | None] = mapped_column(String(100))
    data_prox_atividade: Mapped[datetime | None] = mapped_column(DateTime)
    created_at: Mapped[datetime] = mapped_column(DateTime, server_default=func.now())
    updated_at: Mapped[datetime] = mapped_column(DateTime, server_default=func.now(), onupdate=func.now())
    ativo: Mapped[bool] = mapped_column(Boolean, default=True, server_default=sa.text("true"))

    empresa = relationship("Empresa", foreign_keys=[empresa_id])
    contato_principal = relationship("Contato", foreign_keys=[contato_principal_id])
    origem = relationship("Origem", foreign_keys=[origem_id])
    responsavel = relationship("User", foreign_keys=[responsavel_id])
    atividades = relationship("Atividade", back_populates="lead", cascade="all, delete-orphan")
    historico_etapas = relationship("HistoricoEtapa", back_populates="lead", cascade="all, delete-orphan")
