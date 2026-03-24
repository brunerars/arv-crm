import uuid
from datetime import datetime

from sqlalchemy import String, Integer, Numeric, Boolean, DateTime, Text, ForeignKey, func
import sqlalchemy as sa
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from database import Base


class Empresa(Base):
    __tablename__ = "empresas"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    nome_fantasia: Mapped[str] = mapped_column(String(255), nullable=False)
    razao_social: Mapped[str | None] = mapped_column(String(255))
    cnpj: Mapped[str | None] = mapped_column(String(18), unique=True)
    segmento: Mapped[str | None] = mapped_column(String(100))
    num_funcionarios: Mapped[str | None] = mapped_column(String(50))
    num_plantas: Mapped[int | None] = mapped_column(Integer)
    distancia_arv_km: Mapped[float | None] = mapped_column(Numeric(10, 2))
    cidade: Mapped[str | None] = mapped_column(String(100))
    estado: Mapped[str | None] = mapped_column(String(2))
    cep: Mapped[str | None] = mapped_column(String(10))
    telefone: Mapped[str | None] = mapped_column(String(20))
    site: Mapped[str | None] = mapped_column(String(255))
    status_conta: Mapped[str] = mapped_column(String(30), nullable=False, default="prospect")
    responsavel_id: Mapped[uuid.UUID | None] = mapped_column(UUID(as_uuid=True), ForeignKey("users.id"))
    data_cadastro: Mapped[datetime] = mapped_column(DateTime, server_default=func.now())
    observacoes: Mapped[str | None] = mapped_column(Text)
    created_at: Mapped[datetime] = mapped_column(DateTime, server_default=func.now())
    updated_at: Mapped[datetime] = mapped_column(DateTime, server_default=func.now(), onupdate=func.now())
    ativo: Mapped[bool] = mapped_column(Boolean, default=True, server_default=sa.text("true"))

    contatos = relationship("Contato", back_populates="empresa", cascade="all, delete-orphan")
    responsavel = relationship("User", foreign_keys=[responsavel_id])
