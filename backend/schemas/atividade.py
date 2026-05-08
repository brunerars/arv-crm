import uuid
from datetime import datetime

from pydantic import BaseModel, field_validator, model_validator

from models.atividade import TIPOS_ATIVIDADE, STATUS_ATIVIDADE


class AtividadeCreate(BaseModel):
    lead_id: uuid.UUID | None = None
    oportunidade_id: uuid.UUID | None = None
    empresa_id: uuid.UUID | None = None
    tipo: str
    descricao: str | None = None
    data_prevista: datetime | None = None
    responsavel_id: uuid.UUID | None = None
    geo_uf: str | None = None
    geo_cidade: str | None = None
    geo_zona: str | None = None

    @field_validator("tipo")
    @classmethod
    def validate_tipo(cls, v):
        if v not in TIPOS_ATIVIDADE:
            raise ValueError(f"Tipo deve ser: {', '.join(TIPOS_ATIVIDADE)}")
        return v

    @model_validator(mode="after")
    def validate_target(self):
        if not (self.lead_id or self.oportunidade_id or self.empresa_id):
            raise ValueError("Atividade deve estar vinculada a lead, oportunidade ou empresa")
        return self


class AtividadeUpdate(BaseModel):
    descricao: str | None = None
    data_prevista: datetime | None = None
    data_realizacao: datetime | None = None
    status: str | None = None
    resultado: str | None = None
    geo_uf: str | None = None
    geo_cidade: str | None = None
    geo_zona: str | None = None

    @field_validator("status")
    @classmethod
    def validate_status(cls, v):
        if v is None:
            return v
        if v not in STATUS_ATIVIDADE:
            raise ValueError(f"Status deve ser: {', '.join(STATUS_ATIVIDADE)}")
        return v


class AtividadeResponse(BaseModel):
    id: uuid.UUID
    lead_id: uuid.UUID | None
    oportunidade_id: uuid.UUID | None
    empresa_id: uuid.UUID | None
    responsavel_id: uuid.UUID | None
    criada_por_id: uuid.UUID | None
    tipo: str
    descricao: str | None
    data_prevista: datetime | None
    data_realizacao: datetime | None
    status: str
    resultado: str | None
    geo_uf: str | None
    geo_cidade: str | None
    geo_zona: str | None
    created_at: datetime
    updated_at: datetime

    model_config = {"from_attributes": True}


class AtividadeList(BaseModel):
    items: list[AtividadeResponse]
    total: int
