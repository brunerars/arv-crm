import uuid
from datetime import datetime
from decimal import Decimal

from pydantic import BaseModel, field_validator


class EmpresaCreate(BaseModel):
    nome_fantasia: str
    razao_social: str | None = None
    cnpj: str | None = None
    segmento_mercado_id: uuid.UUID | None = None
    area_atuacao_id: uuid.UUID | None = None
    quantidade_funcionarios: int | None = None
    tempo_mercado_anos: int | None = None
    n_plantas_industriais: int | None = None
    distancia_planta_km: float | None = None
    estado_uf: str | None = None
    cidade: str | None = None
    cep: str | None = None
    endereco_numero: str | None = None
    endereco_complemento: str | None = None
    telefone_fixo: str | None = None
    site: str | None = None
    linkedin: str | None = None
    tipo_id: uuid.UUID | None = None
    is_cliente: bool = False
    responsavel_id: uuid.UUID | None = None
    observacoes: str | None = None

    @field_validator("estado_uf")
    @classmethod
    def validate_uf(cls, v):
        if v is None:
            return v
        if len(v) != 2:
            raise ValueError("estado_uf deve ter 2 caracteres")
        return v.upper()


class EmpresaUpdate(EmpresaCreate):
    nome_fantasia: str | None = None


class EmpresaResponse(BaseModel):
    id: uuid.UUID
    nome_fantasia: str
    razao_social: str | None
    cnpj: str | None
    segmento_mercado_id: uuid.UUID | None
    area_atuacao_id: uuid.UUID | None
    quantidade_funcionarios: int | None
    tempo_mercado_anos: int | None
    n_plantas_industriais: int | None
    distancia_planta_km: Decimal | None
    estado_uf: str | None
    cidade: str | None
    cep: str | None
    endereco_numero: str | None
    endereco_complemento: str | None
    telefone_fixo: str | None
    site: str | None
    linkedin: str | None
    tipo_id: uuid.UUID | None
    is_cliente: bool
    icp_score: Decimal | None
    icp_classificacao: str | None
    responsavel_id: uuid.UUID | None
    observacoes: str | None
    ativo: bool
    created_at: datetime
    updated_at: datetime

    model_config = {"from_attributes": True}


class EmpresaList(BaseModel):
    items: list[EmpresaResponse]
    total: int
