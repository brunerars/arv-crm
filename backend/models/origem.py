import uuid

from sqlalchemy import String
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column

from database import Base


class Origem(Base):
    __tablename__ = "origens"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    tipo: Mapped[str] = mapped_column(String(20), nullable=False)
    sub_tipo: Mapped[str | None] = mapped_column(String(30))
    canal: Mapped[str | None] = mapped_column(String(50))
    descricao: Mapped[str | None] = mapped_column(String(255))
