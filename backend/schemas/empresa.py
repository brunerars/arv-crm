import uuid
from datetime import datetime

from pydantic import BaseModel, field_validator


class EmpresaCreate(BaseModel):
    nome_fantasia: str
    razao_social: str | None = None
    cnpj: str | None = None
    segmento: str | None = None
    num_funcionarios: str | None = None
    num_plantas: int | None = None
    distancia_arv_km: float | None = None
    cidade: str | None = None
    estado: str | None = None
    cep: str | None = None
    telefone: str | None = None
    site: str | None = None
    status_conta: str = "prospect"
    responsavel_id: uuid.UUID | None = None
    observacoes: str | None = None

    @field_validator("status_conta")
    @classmethod
    def validate_status(cls, v):
        allowed = ["prospect", "com_oportunidade", "cliente_ativo", "inativo"]
        if v not in allowed:
            raise ValueError(f"Status deve ser: {', '.join(allowed)}")
        return v


class EmpresaUpdate(EmpresaCreate):
    nome_fantasia: str | None = None


class EmpresaResponse(BaseModel):
    id: uuid.UUID
    nome_fantasia: str
    razao_social: str | None
    cnpj: str | None
    segmento: str | None
    num_funcionarios: str | None
    num_plantas: int | None
    distancia_arv_km: float | None
    cidade: str | None
    estado: str | None
    cep: str | None
    telefone: str | None
    site: str | None
    status_conta: str
    responsavel_id: uuid.UUID | None
    data_cadastro: datetime
    observacoes: str | None
    ativo: bool
    created_at: datetime
    updated_at: datetime

    model_config = {"from_attributes": True}


class EmpresaList(BaseModel):
    items: list[EmpresaResponse]
    total: int
