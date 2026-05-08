import uuid
from datetime import datetime, date

from sqlalchemy import String, Integer, Numeric, DateTime, Date, ForeignKey, func
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from database import Base

ESCOPOS_META = ("GLOBAL", "USER", "ETAPA", "ETAPA_USER")


class MetaVendas(Base):
    __tablename__ = "meta_vendas"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    periodo_inicio: Mapped[date] = mapped_column(Date, nullable=False)
    periodo_fim: Mapped[date] = mapped_column(Date, nullable=False)
    escopo: Mapped[str] = mapped_column(String(20), nullable=False)
    user_id: Mapped[uuid.UUID | None] = mapped_column(UUID(as_uuid=True), ForeignKey("users.id"))
    etapa: Mapped[str | None] = mapped_column(String(40))
    quantidade_meta: Mapped[int | None] = mapped_column(Integer)
    valor_meta: Mapped[float | None] = mapped_column(Numeric(15, 2))
    created_at: Mapped[datetime] = mapped_column(DateTime, server_default=func.now())
    updated_at: Mapped[datetime] = mapped_column(DateTime, server_default=func.now(), onupdate=func.now())

    user = relationship("User", foreign_keys=[user_id])
