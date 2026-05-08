import uuid
from datetime import datetime

from sqlalchemy import String, Integer, Numeric, DateTime, ForeignKey, func
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from database import Base

CATEGORIAS_SCORING = ("TECNICO", "OPORTUNIDADE")


class ScoringResposta(Base):
    __tablename__ = "scoring_respostas"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    lead_id: Mapped[uuid.UUID | None] = mapped_column(UUID(as_uuid=True), ForeignKey("leads.id", ondelete="CASCADE"))
    oportunidade_id: Mapped[uuid.UUID | None] = mapped_column(UUID(as_uuid=True), ForeignKey("oportunidade.id", ondelete="CASCADE"))
    categoria: Mapped[str] = mapped_column(String(20), nullable=False, default="TECNICO", server_default="TECNICO")

    # Schema novo (SPEC §5.2)
    pergunta_codigo: Mapped[str | None] = mapped_column(String(80))
    opcao_codigo: Mapped[str | None] = mapped_column(String(80))
    valor_pontos: Mapped[float | None] = mapped_column(Numeric(6, 2))
    respondido_em: Mapped[datetime | None] = mapped_column(DateTime)
    respondido_por_id: Mapped[uuid.UUID | None] = mapped_column(UUID(as_uuid=True), ForeignKey("users.id"))

    # Legacy mantido ate Macro B refactor (scoring_service.py atual usa)
    criterio: Mapped[str] = mapped_column(String(50), nullable=False)
    valor: Mapped[str] = mapped_column(String(100), nullable=False)
    pontos: Mapped[int] = mapped_column(Integer, nullable=False)
    created_at: Mapped[datetime] = mapped_column(DateTime, server_default=func.now())

    respondido_por = relationship("User", foreign_keys=[respondido_por_id])
