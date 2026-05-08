import uuid
from datetime import datetime, date
from decimal import Decimal

from pydantic import BaseModel, field_validator

from models.oportunidade import ETAPAS_OPORTUNIDADE, TIPOS_ENTREGA, TEMPERATURAS


class OportunidadeCreate(BaseModel):
    empresa_id: uuid.UUID
    lead_id: uuid.UUID | None = None
    responsavel_comercial_id: uuid.UUID | None = None
    responsavel_tecnico_id: uuid.UUID | None = None
    area_atuacao_id: uuid.UUID | None = None
    nome_projeto: str
    descricao_demanda: str | None = None
    produto: str | None = None
    tipo_entrega: str | None = None
    temperatura_comercial: str | None = None
    temperatura_tecnica: str | None = None
    chance_conversao_pct: int | None = None
    nivel_aderencia: str | None = None
    nivel_complexidade: str | None = None
    prazo_emissao_pedido: date | None = None
    prazo_entrega_cliente: date | None = None
    prazo_entrega_arv: date | None = None
    cronograma_inicio: date | None = None
    cronograma_fim: date | None = None
    data_limite_aprovacao_comite: date | None = None
    data_prevista_venda: date | None = None
    visita_alinhamento_tecnico_necessaria: bool = False

    @field_validator("tipo_entrega")
    @classmethod
    def validate_tipo_entrega(cls, v):
        if v is None:
            return v
        if v not in TIPOS_ENTREGA:
            raise ValueError(f"tipo_entrega deve ser: {', '.join(TIPOS_ENTREGA)}")
        return v

    @field_validator("temperatura_comercial", "temperatura_tecnica")
    @classmethod
    def validate_temperatura(cls, v):
        if v is None:
            return v
        if v not in TEMPERATURAS:
            raise ValueError(f"Temperatura deve ser: {', '.join(TEMPERATURAS)}")
        return v

    @field_validator("chance_conversao_pct")
    @classmethod
    def validate_chance(cls, v):
        if v is None:
            return v
        if v < 0 or v > 100:
            raise ValueError("chance_conversao_pct deve estar entre 0 e 100")
        return v


class OportunidadeUpdate(BaseModel):
    responsavel_comercial_id: uuid.UUID | None = None
    responsavel_tecnico_id: uuid.UUID | None = None
    area_atuacao_id: uuid.UUID | None = None
    nome_projeto: str | None = None
    descricao_demanda: str | None = None
    produto: str | None = None
    tipo_entrega: str | None = None
    temperatura_comercial: str | None = None
    temperatura_tecnica: str | None = None
    chance_conversao_pct: int | None = None
    nivel_aderencia: str | None = None
    nivel_complexidade: str | None = None
    prazo_emissao_pedido: date | None = None
    prazo_entrega_cliente: date | None = None
    prazo_entrega_arv: date | None = None
    cronograma_inicio: date | None = None
    cronograma_fim: date | None = None
    data_limite_aprovacao_comite: date | None = None
    data_prevista_venda: date | None = None
    passou_por_comite: bool | None = None
    visita_alinhamento_tecnico_necessaria: bool | None = None
    n_os: str | None = None
    pasta_projeto_atualizada: bool | None = None
    acao_recomendada: str | None = None

    @field_validator("tipo_entrega")
    @classmethod
    def validate_tipo_entrega(cls, v):
        if v is None:
            return v
        if v not in TIPOS_ENTREGA:
            raise ValueError(f"tipo_entrega deve ser: {', '.join(TIPOS_ENTREGA)}")
        return v

    @field_validator("temperatura_comercial", "temperatura_tecnica")
    @classmethod
    def validate_temperatura(cls, v):
        if v is None:
            return v
        if v not in TEMPERATURAS:
            raise ValueError(f"Temperatura deve ser: {', '.join(TEMPERATURAS)}")
        return v


class OportunidadeResponse(BaseModel):
    id: uuid.UUID
    oportunidade_id: str
    empresa_id: uuid.UUID
    lead_id: uuid.UUID | None
    responsavel_comercial_id: uuid.UUID | None
    responsavel_tecnico_id: uuid.UUID | None
    area_atuacao_id: uuid.UUID | None
    nome_projeto: str
    descricao_demanda: str | None
    produto: str | None
    tipo_entrega: str | None
    etapa: str
    data_handoff: datetime | None
    data_ultima_atividade: datetime | None
    descartado: bool
    motivo_descarte: str | None
    data_descarte: datetime | None
    data_reativacao: datetime | None
    status_reativacao: str | None
    score_tecnico: Decimal | None
    score_oportunidade: Decimal | None
    temperatura_comercial: str | None
    temperatura_tecnica: str | None
    acao_recomendada: str | None
    chance_conversao_pct: int | None
    data_prevista_venda: date | None
    data_conclusao: datetime | None
    nivel_aderencia: str | None
    nivel_complexidade: str | None
    prazo_emissao_pedido: date | None
    prazo_entrega_cliente: date | None
    prazo_entrega_arv: date | None
    cronograma_inicio: date | None
    cronograma_fim: date | None
    data_limite_aprovacao_comite: date | None
    passou_por_comite: bool
    visita_alinhamento_tecnico_necessaria: bool
    n_revisao: int
    n_os: str | None
    pasta_projeto_atualizada: bool
    ativo: bool
    created_at: datetime
    updated_at: datetime

    model_config = {"from_attributes": True}


class KanbanColumn(BaseModel):
    etapa: str
    count: int
    oportunidades: list[OportunidadeResponse]


class KanbanResponse(BaseModel):
    columns: list[KanbanColumn]
    total_oportunidades: int


class ChangeStageRequest(BaseModel):
    nova_etapa: str

    @field_validator("nova_etapa")
    @classmethod
    def validate_etapa(cls, v):
        if v not in ETAPAS_OPORTUNIDADE:
            raise ValueError(f"Etapa deve ser: {', '.join(ETAPAS_OPORTUNIDADE)}")
        return v


class HistoricoOportunidadeResponse(BaseModel):
    id: uuid.UUID
    etapa: str
    entrou_em: datetime
    saiu_em: datetime | None
    responsavel_no_periodo_id: uuid.UUID | None

    model_config = {"from_attributes": True}
