"""SPEC §1.3 — Orçamento como entidade própria com versionamento (1 Oportunidade : N Orçamentos).

Corrige bug do legado Monday onde "Proposta sem Imposto" somava IR/CSLL.
IR/CSLL são tributos sobre lucro — não compõem preço de venda.
Apenas tributos sobre vendas (ICMS, ISS, PIS, COFINS) entram em valor_com_imposto.
"""
import uuid
from decimal import Decimal

from sqlalchemy import select, func
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from models.orcamento import Orcamento
from models.oportunidade import Oportunidade


def _calc_valores(orc: Orcamento) -> tuple[Decimal, Decimal]:
    """Retorna (valor_sem_imposto, valor_com_imposto).

    valor_sem_imposto = custos diretos + comissao + markup (sem nenhum imposto)
    valor_com_imposto = valor_sem_imposto * (1 + tributos_venda%)
    IR/CSLL ficam guardados em pct mas NÃO entram no preço (corrige bug legado).
    """
    base = Decimal(orc.valor_base or 0)
    custos = (
        Decimal(orc.custo_fixo or 0)
        + Decimal(orc.custo_financeiro or 0)
        + Decimal(orc.custo_terceiros or 0)
        + Decimal(orc.custo_mao_obra or 0)
        + Decimal(orc.cmv_estimado or 0)
    )
    comissao_brl = base * Decimal(orc.comissao_pct or 0) / Decimal(100)
    markup_brl = base * Decimal(orc.markup_pct or 0) / Decimal(100)

    valor_sem = custos + comissao_brl + markup_brl

    tributos_venda_pct = (
        Decimal(orc.icms_pct or 0)
        + Decimal(orc.iss_pct or 0)
        + Decimal(orc.pis_pct or 0)
        + Decimal(orc.cofins_pct or 0)
    )
    valor_com = valor_sem * (Decimal(1) + tributos_venda_pct / Decimal(100))

    return valor_sem.quantize(Decimal("0.01")), valor_com.quantize(Decimal("0.01"))


class OrcamentoService:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def _next_versao(self, oportunidade_id: uuid.UUID) -> int:
        result = await self.db.execute(
            select(func.max(Orcamento.versao)).where(Orcamento.oportunidade_id == oportunidade_id)
        )
        atual = result.scalar()
        return (atual or 0) + 1

    async def list_by_oportunidade(self, oportunidade_id: uuid.UUID) -> list[Orcamento]:
        result = await self.db.execute(
            select(Orcamento)
            .where(Orcamento.oportunidade_id == oportunidade_id)
            .order_by(Orcamento.versao.desc())
        )
        return list(result.scalars().all())

    async def get(self, orcamento_id: uuid.UUID) -> Orcamento | None:
        result = await self.db.execute(select(Orcamento).where(Orcamento.id == orcamento_id))
        return result.scalar_one_or_none()

    async def create(
        self,
        oportunidade_id: uuid.UUID,
        data: dict,
        user_id: uuid.UUID,
    ) -> Orcamento:
        opp = await self.db.execute(select(Oportunidade).where(Oportunidade.id == oportunidade_id))
        if not opp.scalar_one_or_none():
            raise ValueError("Oportunidade nao encontrada")

        versao = await self._next_versao(oportunidade_id)
        orc = Orcamento(
            oportunidade_id=oportunidade_id,
            versao=versao,
            criado_por_id=user_id,
            **data,
        )
        valor_sem, valor_com = _calc_valores(orc)
        orc.valor_sem_imposto = valor_sem
        orc.valor_com_imposto = valor_com

        self.db.add(orc)
        await self.db.commit()
        await self.db.refresh(orc)
        return orc

    async def update(self, orcamento_id: uuid.UUID, data: dict) -> Orcamento:
        orc = await self.get(orcamento_id)
        if not orc:
            raise ValueError("Orcamento nao encontrado")

        for key, value in data.items():
            setattr(orc, key, value)

        valor_sem, valor_com = _calc_valores(orc)
        orc.valor_sem_imposto = valor_sem
        orc.valor_com_imposto = valor_com

        await self.db.commit()
        await self.db.refresh(orc)
        return orc

    async def delete(self, orcamento_id: uuid.UUID) -> None:
        """Hard delete — orçamento não tem flag ativo. Versão fica fora de sequência (gap),
        é OK porque versionamento é monotônico, não denso."""
        orc = await self.get(orcamento_id)
        if not orc:
            raise ValueError("Orcamento nao encontrado")
        await self.db.delete(orc)
        await self.db.commit()

    async def duplicar(self, orcamento_id: uuid.UUID, user_id: uuid.UUID) -> Orcamento:
        """Cria nova versão a partir de orçamento existente (mesma oportunidade).
        Reseta flags de envio/aprovação para que a nova versão comece "limpa"."""
        origem = await self.get(orcamento_id)
        if not origem:
            raise ValueError("Orcamento nao encontrado")

        nova_versao = await self._next_versao(origem.oportunidade_id)
        nova = Orcamento(
            oportunidade_id=origem.oportunidade_id,
            versao=nova_versao,
            status_id=origem.status_id,
            valor_base=origem.valor_base,
            custo_fixo=origem.custo_fixo,
            custo_financeiro=origem.custo_financeiro,
            custo_terceiros=origem.custo_terceiros,
            custo_mao_obra=origem.custo_mao_obra,
            cmv_estimado=origem.cmv_estimado,
            comissao_pct=origem.comissao_pct,
            markup_pct=origem.markup_pct,
            ir_pct=origem.ir_pct,
            csll_pct=origem.csll_pct,
            icms_pct=origem.icms_pct,
            iss_pct=origem.iss_pct,
            pis_pct=origem.pis_pct,
            cofins_pct=origem.cofins_pct,
            antecipacao_prevista=origem.antecipacao_prevista,
            prazo_avaliacao_tecnica_cliente=origem.prazo_avaliacao_tecnica_cliente,
            prazo_analise_comercial_cliente=origem.prazo_analise_comercial_cliente,
            criado_por_id=user_id,
        )
        valor_sem, valor_com = _calc_valores(nova)
        nova.valor_sem_imposto = valor_sem
        nova.valor_com_imposto = valor_com

        self.db.add(nova)
        await self.db.commit()
        await self.db.refresh(nova)
        return nova
