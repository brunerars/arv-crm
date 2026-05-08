import uuid
from datetime import datetime

from pydantic import BaseModel, field_validator

from schemas.empresa import EmpresaResponse
from schemas.contato import ContatoResponse

ETAPAS_LEAD = (
    "LEAD_INICIAL",
    "ANALISE_INTERNA",
    "QUALIFICACAO_INICIAL",
    "QUALIFICACAO_OPORTUNIDADE",
)
TEMPERATURAS = ("frio", "morno", "quente")


class LeadCreate(BaseModel):
    empresa_id: uuid.UUID
    contato_principal_id: uuid.UUID | None = None
    origem_id: uuid.UUID | None = None
    sub_origem_canal: str | None = None
    responsavel_pre_vendas_id: uuid.UUID | None = None
    nome_projeto: str | None = None
    descricao_demanda: str | None = None
    produto_interesse: str | None = None
    area_atuacao: str | None = None
    tipo_entrega: str | None = None
    temperatura: str = "frio"
    valor_estimado: float = 0

    @field_validator("temperatura")
    @classmethod
    def validate_temperatura(cls, v):
        if v not in TEMPERATURAS:
            raise ValueError(f"Temperatura deve ser: {', '.join(TEMPERATURAS)}")
        return v


class LeadUpdate(BaseModel):
    contato_principal_id: uuid.UUID | None = None
    origem_id: uuid.UUID | None = None
    sub_origem_canal: str | None = None
    responsavel_pre_vendas_id: uuid.UUID | None = None
    nome_projeto: str | None = None
    descricao_demanda: str | None = None
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
    sub_origem_canal: str | None
    responsavel_pre_vendas_id: uuid.UUID | None
    nome_projeto: str | None
    descricao_demanda: str | None
    etapa: str
    sub_status: str | None
    temperatura: str
    produto_interesse: str | None
    area_atuacao: str | None
    tipo_entrega: str | None
    lead_score: int
    classificacao: str | None
    valor_estimado: float
    descartado: bool
    motivo_descarte: str | None
    data_descarte: datetime | None
    data_reativacao: datetime | None
    status_reativacao: str | None
    data_entrada_pre_vendas: datetime
    data_qualificacao: datetime | None
    data_ultima_atividade: datetime | None
    passou_por_comite: bool
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
    etapa: str
    entrou_em: datetime
    saiu_em: datetime | None
    responsavel_no_periodo_id: uuid.UUID | None

    model_config = {"from_attributes": True}
