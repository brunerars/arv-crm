import uuid
from datetime import datetime

from sqlalchemy import select, text
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from models.oportunidade import Oportunidade, ETAPAS_OPORTUNIDADE
from models.empresa import Empresa
from models.historico_etapa import HistoricoEtapaOportunidade
from schemas.oportunidade import (
    OportunidadeCreate,
    KanbanResponse,
    KanbanColumn,
    OportunidadeResponse,
)

ETAPAS_ORDER = list(ETAPAS_OPORTUNIDADE)


class OportunidadeService:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def generate_oportunidade_id(self) -> str:
        result = await self.db.execute(text("SELECT nextval('oportunidade_id_seq')"))
        seq = result.scalar()
        return f"OPP-{seq:04d}"

    async def create_oportunidade(self, data: OportunidadeCreate, user_id: uuid.UUID) -> Oportunidade:
        emp = await self.db.execute(select(Empresa).where(Empresa.id == data.empresa_id))
        if not emp.scalar_one_or_none():
            raise ValueError("Empresa nao encontrada")

        oportunidade_id = await self.generate_oportunidade_id()
        opp = Oportunidade(
            oportunidade_id=oportunidade_id,
            **data.model_dump(),
        )
        if not opp.responsavel_comercial_id:
            opp.responsavel_comercial_id = user_id
        self.db.add(opp)
        await self.db.flush()

        historico = HistoricoEtapaOportunidade(
            oportunidade_id=opp.id,
            etapa="ESTIMATIVA",
            entrou_em=datetime.utcnow(),
            responsavel_no_periodo_id=opp.responsavel_comercial_id,
        )
        self.db.add(historico)
        await self.db.commit()
        await self.db.refresh(opp)
        return opp

    async def _close_current_history(self, oportunidade_id: uuid.UUID) -> None:
        result = await self.db.execute(
            select(HistoricoEtapaOportunidade)
            .where(HistoricoEtapaOportunidade.oportunidade_id == oportunidade_id)
            .where(HistoricoEtapaOportunidade.saiu_em.is_(None))
        )
        for entry in result.scalars().all():
            entry.saiu_em = datetime.utcnow()

    async def change_stage(
        self,
        oportunidade_id: uuid.UUID,
        nova_etapa: str,
        user_id: uuid.UUID,
    ) -> Oportunidade:
        if nova_etapa not in ETAPAS_ORDER:
            raise ValueError(f"Etapa invalida: {nova_etapa}")

        result = await self.db.execute(select(Oportunidade).where(Oportunidade.id == oportunidade_id))
        opp = result.scalar_one_or_none()
        if not opp:
            raise ValueError("Oportunidade nao encontrada")
        if opp.descartado:
            raise ValueError(
                "Oportunidade descartada nao pode mudar de etapa. "
                "Reative primeiro via POST /oportunidades/{id}/reativar"
            )

        await self._close_current_history(opp.id)

        novo_hist = HistoricoEtapaOportunidade(
            oportunidade_id=opp.id,
            etapa=nova_etapa,
            entrou_em=datetime.utcnow(),
            responsavel_no_periodo_id=opp.responsavel_comercial_id,
        )
        self.db.add(novo_hist)

        opp.etapa = nova_etapa
        if nova_etapa == "CONVERTIDA_EM_VENDA":
            opp.data_conclusao = datetime.utcnow()

        await self.db.commit()
        await self.db.refresh(opp)
        return opp

    async def get_kanban(
        self,
        responsavel_comercial_id: uuid.UUID | None = None,
        responsavel_tecnico_id: uuid.UUID | None = None,
        temperatura_comercial: str | None = None,
        search: str | None = None,
        incluir_descartados: bool = False,
    ) -> KanbanResponse:
        query = (
            select(Oportunidade)
            .options(selectinload(Oportunidade.empresa))
            .where(Oportunidade.ativo == True)
        )
        if not incluir_descartados:
            query = query.where(Oportunidade.descartado == False)

        if responsavel_comercial_id:
            query = query.where(Oportunidade.responsavel_comercial_id == responsavel_comercial_id)
        if responsavel_tecnico_id:
            query = query.where(Oportunidade.responsavel_tecnico_id == responsavel_tecnico_id)
        if temperatura_comercial:
            query = query.where(Oportunidade.temperatura_comercial == temperatura_comercial)
        if search:
            query = query.join(Empresa).where(Empresa.nome_fantasia.ilike(f"%{search}%"))

        result = await self.db.execute(query.order_by(Oportunidade.created_at.desc()))
        oportunidades = result.scalars().all()

        columns = []
        total = 0
        for etapa in ETAPAS_ORDER:
            etapa_opps = [o for o in oportunidades if o.etapa == etapa]
            columns.append(KanbanColumn(
                etapa=etapa,
                count=len(etapa_opps),
                oportunidades=[OportunidadeResponse.model_validate(o) for o in etapa_opps],
            ))
            total += len(etapa_opps)

        return KanbanResponse(columns=columns, total_oportunidades=total)
