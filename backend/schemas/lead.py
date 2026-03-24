import uuid
from datetime import datetime

from pydantic import BaseModel, field_validator

from schemas.empresa import EmpresaResponse
from schemas.contato import ContatoResponse


class LeadCreate(BaseModel):
    empresa_id: uuid.UUID
    contato_principal_id: uuid.UUID | None = None
    origem_id: uuid.UUID | None = None
    responsavel_id: uuid.UUID | None = None
    temperatura: str = "frio"
    produto_interesse: str | None = None
    area_atuacao: str | None = None
    tipo_entrega: str | None = None
    valor_estimado: float = 0

    @field_validator("temperatura")
    @classmethod
    def validate_temperatura(cls, v):
        allowed = ["frio", "morno", "quente"]
        if v not in allowed:
            raise ValueError(f"Temperatura deve ser: {', '.join(allowed)}")
        return v


class LeadUpdate(BaseModel):
    contato_principal_id: uuid.UUID | None = None
    origem_id: uuid.UUID | None = None
    responsavel_id: uuid.UUID | None = None
    temperatura: str | None = None
    produto_interesse: str | None = None
    area_atuacao: str | None = None
    tipo_entrega: str | None = None
    valor_estimado: float | None = None
    motivo_descarte: str | None = None
    prox_atividade: str | None = None
    data_prox_atividade: datetime | None = None
    sub_status: str | None = None


class LeadResponse(BaseModel):
    id: uuid.UUID
    lead_id: str
    empresa_id: uuid.UUID
    contato_principal_id: uuid.UUID | None
    origem_id: uuid.UUID | None
    responsavel_id: uuid.UUID | None
    etapa: str
    sub_status: str | None
    temperatura: str
    produto_interesse: str | None
    area_atuacao: str | None
    tipo_entrega: str | None
    lead_score: int
    classificacao: str | None
    valor_estimado: float
    motivo_descarte: str | None
    data_entrada: datetime
    data_qualificacao: datetime | None
    prox_atividade: str | None
    data_prox_atividade: datetime | None
    ativo: bool
    created_at: datetime
    updated_at: datetime

    model_config = {"from_attributes": True}


class LeadDetail(LeadResponse):
    empresa: EmpresaResponse | None = None
    contato_principal: ContatoResponse | None = None
    completude: dict | None = None


class KanbanColumn(BaseModel):
    etapa: str
    count: int
    total_valor: float
    leads: list[LeadResponse]


class KanbanResponse(BaseModel):
    columns: list[KanbanColumn]
    total_leads: int
    total_valor: float


class ChangeStageRequest(BaseModel):
    nova_etapa: str
    motivo_descarte: str | None = None


class Completude(BaseModel):
    etapa: str
    pct: float
    filled: list[str]
    missing: list[str]
    total: int


class HistoricoResponse(BaseModel):
    id: uuid.UUID
    etapa_anterior: str | None
    etapa_nova: str
    tempo_na_etapa_segundos: int | None
    created_at: datetime

    model_config = {"from_attributes": True}
