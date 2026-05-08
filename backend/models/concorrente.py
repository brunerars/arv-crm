import uuid
from datetime import datetime

from sqlalchemy import String, Integer, Boolean, DateTime, Text, func
import sqlalchemy as sa
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column

from database import Base


class Concorrente(Base):
    __tablename__ = "concorrente"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    cnpj: Mapped[str | None] = mapped_column(String(18), unique=True)
    nome: Mapped[str] = mapped_column(String(255), nullable=False)
    uf: Mapped[str | None] = mapped_column(String(2))
    cidade: Mapped[str | None] = mapped_column(String(100))
    qtde_filiais: Mapped[int | None] = mapped_column(Integer)
    n_funcionarios_faixa: Mapped[str | None] = mapped_column(String(50))
    fundacao_ano: Mapped[int | None] = mapped_column(Integer)
    portfolio: Mapped[str | None] = mapped_column(Text)
    principais_clientes: Mapped[str | None] = mapped_column(Text)
    principais_parceiros: Mapped[str | None] = mapped_column(Text)
    observacoes: Mapped[str | None] = mapped_column(Text)
    ativo: Mapped[bool] = mapped_column(Boolean, nullable=False, default=True, server_default=sa.text("true"))
    created_at: Mapped[datetime] = mapped_column(DateTime, server_default=func.now())
    updated_at: Mapped[datetime] = mapped_column(DateTime, server_default=func.now(), onupdate=func.now())
