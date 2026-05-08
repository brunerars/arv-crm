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

    segmento_mercado_id: Mapped[uuid.UUID | None] = mapped_column(UUID(as_uuid=True), ForeignKey("segmento_mercado.id"))
    area_atuacao_id: Mapped[uuid.UUID | None] = mapped_column(UUID(as_uuid=True), ForeignKey("area_atuacao.id"))
    quantidade_funcionarios: Mapped[int | None] = mapped_column(Integer)
    tempo_mercado_anos: Mapped[int | None] = mapped_column(Integer)
    n_plantas_industriais: Mapped[int | None] = mapped_column(Integer)
    distancia_planta_km: Mapped[float | None] = mapped_column(Numeric(10, 2))

    estado_uf: Mapped[str | None] = mapped_column(String(2))
    cidade: Mapped[str | None] = mapped_column(String(100))
    cep: Mapped[str | None] = mapped_column(String(10))
    endereco_numero: Mapped[str | None] = mapped_column(String(20))
    endereco_complemento: Mapped[str | None] = mapped_column(String(100))

    telefone_fixo: Mapped[str | None] = mapped_column(String(20))
    site: Mapped[str | None] = mapped_column(String(255))
    linkedin: Mapped[str | None] = mapped_column(String(255))

    tipo_id: Mapped[uuid.UUID | None] = mapped_column(UUID(as_uuid=True), ForeignKey("tipo_empresa.id"))
    is_cliente: Mapped[bool] = mapped_column(Boolean, nullable=False, default=False, server_default=sa.text("false"))
    icp_score: Mapped[float | None] = mapped_column(Numeric(5, 2))
    icp_classificacao: Mapped[str | None] = mapped_column(String(1))

    responsavel_id: Mapped[uuid.UUID | None] = mapped_column(UUID(as_uuid=True), ForeignKey("users.id"))
    ativo: Mapped[bool] = mapped_column(Boolean, default=True, server_default=sa.text("true"))
    observacoes: Mapped[str | None] = mapped_column(Text)
    created_at: Mapped[datetime] = mapped_column(DateTime, server_default=func.now())
    updated_at: Mapped[datetime] = mapped_column(DateTime, server_default=func.now(), onupdate=func.now())

    contatos = relationship("Contato", back_populates="empresa", cascade="all, delete-orphan")
    responsavel = relationship("User", foreign_keys=[responsavel_id])
    segmento_mercado = relationship("SegmentoMercado", foreign_keys=[segmento_mercado_id])
    area_atuacao = relationship("AreaAtuacao", foreign_keys=[area_atuacao_id])
    tipo = relationship("TipoEmpresa", foreign_keys=[tipo_id])
