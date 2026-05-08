import uuid
from datetime import datetime

from sqlalchemy import String, DateTime, ForeignKey, func
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from database import Base


class HistoricoEtapaLead(Base):
    __tablename__ = "historico_etapa_lead"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    lead_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), ForeignKey("leads.id", ondelete="CASCADE"), nullable=False)
    etapa: Mapped[str] = mapped_column(String(40), nullable=False)
    entrou_em: Mapped[datetime] = mapped_column(DateTime, nullable=False, server_default=func.now())
    saiu_em: Mapped[datetime | None] = mapped_column(DateTime)
    responsavel_no_periodo_id: Mapped[uuid.UUID | None] = mapped_column(UUID(as_uuid=True), ForeignKey("users.id"))

    lead = relationship("Lead", back_populates="historico_etapas")
    responsavel_no_periodo = relationship("User", foreign_keys=[responsavel_no_periodo_id])


class HistoricoEtapaOportunidade(Base):
    __tablename__ = "historico_etapa_oportunidade"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    oportunidade_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), ForeignKey("oportunidade.id", ondelete="CASCADE"), nullable=False)
    etapa: Mapped[str] = mapped_column(String(40), nullable=False)
    entrou_em: Mapped[datetime] = mapped_column(DateTime, nullable=False, server_default=func.now())
    saiu_em: Mapped[datetime | None] = mapped_column(DateTime)
    responsavel_no_periodo_id: Mapped[uuid.UUID | None] = mapped_column(UUID(as_uuid=True), ForeignKey("users.id"))

    oportunidade = relationship("Oportunidade", foreign_keys=[oportunidade_id])
    responsavel_no_periodo = relationship("User", foreign_keys=[responsavel_no_periodo_id])
