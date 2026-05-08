import uuid
from datetime import datetime

from sqlalchemy import String, DateTime, Text, ForeignKey, func
import sqlalchemy as sa
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from database import Base

TIPOS_ATIVIDADE = (
    "email",
    "ligacao",
    "reuniao_interna",
    "passagem_bastao",
    "tarefa",
    "tarefa_tecnica",
    "visita_comercial",
    "visita_tecnica",
    "apresentacao_proposta",
)
STATUS_ATIVIDADE = ("planejada", "em_andamento", "realizada", "cancelada")


class Atividade(Base):
    __tablename__ = "atividades"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    lead_id: Mapped[uuid.UUID | None] = mapped_column(UUID(as_uuid=True), ForeignKey("leads.id", ondelete="CASCADE"))
    oportunidade_id: Mapped[uuid.UUID | None] = mapped_column(UUID(as_uuid=True), ForeignKey("oportunidade.id", ondelete="CASCADE"))
    empresa_id: Mapped[uuid.UUID | None] = mapped_column(UUID(as_uuid=True), ForeignKey("empresas.id"))

    responsavel_id: Mapped[uuid.UUID | None] = mapped_column(UUID(as_uuid=True), ForeignKey("users.id"))
    criada_por_id: Mapped[uuid.UUID | None] = mapped_column(UUID(as_uuid=True), ForeignKey("users.id"))

    tipo: Mapped[str] = mapped_column(String(50), nullable=False)
    descricao: Mapped[str | None] = mapped_column(Text)
    data_prevista: Mapped[datetime | None] = mapped_column(DateTime)
    data_realizacao: Mapped[datetime | None] = mapped_column(DateTime)
    status: Mapped[str] = mapped_column(String(20), nullable=False, default="planejada", server_default="planejada")
    resultado: Mapped[str | None] = mapped_column(Text)

    geo_uf: Mapped[str | None] = mapped_column(String(2))
    geo_cidade: Mapped[str | None] = mapped_column(String(100))
    geo_zona: Mapped[str | None] = mapped_column(String(80))

    created_at: Mapped[datetime] = mapped_column(DateTime, server_default=func.now())
    updated_at: Mapped[datetime] = mapped_column(DateTime, server_default=func.now(), onupdate=func.now())

    lead = relationship("Lead", back_populates="atividades")
    oportunidade = relationship("Oportunidade", foreign_keys=[oportunidade_id])
    empresa = relationship("Empresa", foreign_keys=[empresa_id])
    responsavel = relationship("User", foreign_keys=[responsavel_id])
    criada_por = relationship("User", foreign_keys=[criada_por_id])
