import uuid
from datetime import datetime, date
from decimal import Decimal

from pydantic import BaseModel, field_validator


def _validate_pct(v):
    if v is None:
        return v
    if v < 0 or v > 100:
        raise ValueError("percentual deve estar entre 0 e 100")
    return v


class OrcamentoBase(BaseModel):
    status_id: uuid.UUID | None = None

    valor_base: Decimal = Decimal(0)
    custo_fixo: Decimal = Decimal(0)
    custo_financeiro: Decimal = Decimal(0)
    custo_terceiros: Decimal = Decimal(0)
    custo_mao_obra: Decimal = Decimal(0)
    cmv_estimado: Decimal = Decimal(0)

    comissao_pct: Decimal = Decimal(0)
    markup_pct: Decimal = Decimal(0)

    ir_pct: Decimal = Decimal(0)
    csll_pct: Decimal = Decimal(0)
    icms_pct: Decimal = Decimal(0)
    iss_pct: Decimal = Decimal(0)
    pis_pct: Decimal = Decimal(0)
    cofins_pct: Decimal = Decimal(0)

    antecipacao_prevista: Decimal | None = None
    antecipacao_confirmada: Decimal | None = None
    data_recebimento_antecipacao: date | None = None

    foi_enviado_cliente: bool = False
    data_envio: datetime | None = None
    cliente_confirmou_recebimento: bool = False
    prazo_avaliacao_tecnica_cliente: date | None = None
    solucao_tecnica_aprovada: bool = False
    prazo_analise_comercial_cliente: date | None = None
    email_enviado_comprador: bool = False
    condicoes_comerciais_aceitas: bool = False
    cliente_confirmou_intencao_compra: bool = False

    @field_validator(
        "comissao_pct", "markup_pct",
        "ir_pct", "csll_pct", "icms_pct", "iss_pct", "pis_pct", "cofins_pct",
    )
    @classmethod
    def validate_percentuais(cls, v):
        return _validate_pct(v)


class OrcamentoCreate(OrcamentoBase):
    pass


class OrcamentoUpdate(BaseModel):
    status_id: uuid.UUID | None = None

    valor_base: Decimal | None = None
    custo_fixo: Decimal | None = None
    custo_financeiro: Decimal | None = None
    custo_terceiros: Decimal | None = None
    custo_mao_obra: Decimal | None = None
    cmv_estimado: Decimal | None = None

    comissao_pct: Decimal | None = None
    markup_pct: Decimal | None = None

    ir_pct: Decimal | None = None
    csll_pct: Decimal | None = None
    icms_pct: Decimal | None = None
    iss_pct: Decimal | None = None
    pis_pct: Decimal | None = None
    cofins_pct: Decimal | None = None

    antecipacao_prevista: Decimal | None = None
    antecipacao_confirmada: Decimal | None = None
    data_recebimento_antecipacao: date | None = None

    foi_enviado_cliente: bool | None = None
    data_envio: datetime | None = None
    cliente_confirmou_recebimento: bool | None = None
    prazo_avaliacao_tecnica_cliente: date | None = None
    solucao_tecnica_aprovada: bool | None = None
    prazo_analise_comercial_cliente: date | None = None
    email_enviado_comprador: bool | None = None
    condicoes_comerciais_aceitas: bool | None = None
    cliente_confirmou_intencao_compra: bool | None = None

    @field_validator(
        "comissao_pct", "markup_pct",
        "ir_pct", "csll_pct", "icms_pct", "iss_pct", "pis_pct", "cofins_pct",
    )
    @classmethod
    def validate_percentuais(cls, v):
        return _validate_pct(v)


class OrcamentoResponse(BaseModel):
    id: uuid.UUID
    oportunidade_id: uuid.UUID
    versao: int
    status_id: uuid.UUID | None

    valor_base: Decimal
    custo_fixo: Decimal
    custo_financeiro: Decimal
    custo_terceiros: Decimal
    custo_mao_obra: Decimal
    cmv_estimado: Decimal

    comissao_pct: Decimal
    markup_pct: Decimal

    ir_pct: Decimal
    csll_pct: Decimal
    icms_pct: Decimal
    iss_pct: Decimal
    pis_pct: Decimal
    cofins_pct: Decimal

    valor_com_imposto: Decimal | None
    valor_sem_imposto: Decimal | None

    antecipacao_prevista: Decimal | None
    antecipacao_confirmada: Decimal | None
    data_recebimento_antecipacao: date | None

    foi_enviado_cliente: bool
    data_envio: datetime | None
    cliente_confirmou_recebimento: bool
    prazo_avaliacao_tecnica_cliente: date | None
    solucao_tecnica_aprovada: bool
    prazo_analise_comercial_cliente: date | None
    email_enviado_comprador: bool
    condicoes_comerciais_aceitas: bool
    cliente_confirmou_intencao_compra: bool

    criado_por_id: uuid.UUID | None
    created_at: datetime
    updated_at: datetime

    model_config = {"from_attributes": True}
