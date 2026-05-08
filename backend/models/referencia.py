"""Tabelas de referencia (lookup) usadas como FKs em entidades de dominio.

Populadas via script separado `backend/scripts/seed_referencias.py` a partir
de DADOS-VENDAS.xlsx sheet "Tabelas de Apoio" (SPEC §12 Macro A).
"""
import uuid
from datetime import datetime

from sqlalchemy import String, Boolean, Integer, DateTime, Text, func
import sqlalchemy as sa
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column

from database import Base


class SegmentoMercado(Base):
    __tablename__ = "segmento_mercado"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    nome: Mapped[str] = mapped_column(String(150), nullable=False, unique=True)
    descricao: Mapped[str | None] = mapped_column(Text)
    ativo: Mapped[bool] = mapped_column(Boolean, nullable=False, default=True, server_default=sa.text("true"))
    created_at: Mapped[datetime] = mapped_column(DateTime, server_default=func.now())


class AreaAtuacao(Base):
    __tablename__ = "area_atuacao"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    nome: Mapped[str] = mapped_column(String(150), nullable=False, unique=True)
    descricao: Mapped[str | None] = mapped_column(Text)
    ativo: Mapped[bool] = mapped_column(Boolean, nullable=False, default=True, server_default=sa.text("true"))
    created_at: Mapped[datetime] = mapped_column(DateTime, server_default=func.now())


class TipoEmpresa(Base):
    __tablename__ = "tipo_empresa"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    nome: Mapped[str] = mapped_column(String(80), nullable=False, unique=True)
    descricao: Mapped[str | None] = mapped_column(Text)
    ativo: Mapped[bool] = mapped_column(Boolean, nullable=False, default=True, server_default=sa.text("true"))
    created_at: Mapped[datetime] = mapped_column(DateTime, server_default=func.now())


class StatusOrcamento(Base):
    __tablename__ = "status_orcamento"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    nome: Mapped[str] = mapped_column(String(80), nullable=False, unique=True)
    descricao: Mapped[str | None] = mapped_column(Text)
    ordem: Mapped[int] = mapped_column(Integer, nullable=False, default=0, server_default="0")
    ativo: Mapped[bool] = mapped_column(Boolean, nullable=False, default=True, server_default=sa.text("true"))
    created_at: Mapped[datetime] = mapped_column(DateTime, server_default=func.now())


class EquipeComercial(Base):
    __tablename__ = "equipe_comercial"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    nome: Mapped[str] = mapped_column(String(120), nullable=False, unique=True)
    descricao: Mapped[str | None] = mapped_column(Text)
    ativo: Mapped[bool] = mapped_column(Boolean, nullable=False, default=True, server_default=sa.text("true"))
    created_at: Mapped[datetime] = mapped_column(DateTime, server_default=func.now())
