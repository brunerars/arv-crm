import uuid
from datetime import datetime

from sqlalchemy import String, Integer, DateTime, ForeignKey, func
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from database import Base


class HistoricoEtapa(Base):
    __tablename__ = "historico_etapas"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    lead_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), ForeignKey("leads.id", ondelete="CASCADE"), nullable=False)
    etapa_anterior: Mapped[str | None] = mapped_column(String(30))
    etapa_nova: Mapped[str] = mapped_column(String(30), nullable=False)
    tempo_na_etapa_segundos: Mapped[int | None] = mapped_column(Integer)
    usuario_id: Mapped[uuid.UUID | None] = mapped_column(UUID(as_uuid=True), ForeignKey("users.id"))
    created_at: Mapped[datetime] = mapped_column(DateTime, server_default=func.now())

    lead = relationship("Lead", back_populates="historico_etapas")
    usuario = relationship("User", foreign_keys=[usuario_id])
