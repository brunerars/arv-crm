import uuid
from datetime import datetime

from sqlalchemy import select, text
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from models.lead import Lead, ETAPAS_LEAD
from models.empresa import Empresa
from models.historico_etapa import HistoricoEtapaLead
from schemas.lead import LeadCreate, KanbanResponse, KanbanColumn, LeadResponse, Completude

ETAPAS_ORDER = list(ETAPAS_LEAD)

# SPEC §4.1 - travas pre-vendas. Implementacao formal em B2 (stage_validators.py).
# Aqui mantenho apenas o calculo de completude visual (UI).
COMPLETUDE_MAP = {
    "LEAD_INICIAL": {
        "empresa.nome_fantasia": "Nome da empresa",
        "empresa.cnpj": "CNPJ",
        "origem_id": "Origem",
        "sub_origem_canal": "Canal da origem",
        "empresa.telefone_fixo": "Telefone fixo",
        "contato_principal.nome": "Nome do contato",
        "contato_principal.telefone_whatsapp": "Telefone/WhatsApp",
        "contato_principal.email": "E-mail",
    },
    "ANALISE_INTERNA": {},
    "QUALIFICACAO_INICIAL": {
        "empresa.segmento_mercado_id": "Segmento de mercado",
        "empresa.tempo_mercado_anos": "Tempo de mercado",
        "empresa.distancia_planta_km": "Distancia da planta (km)",
        "empresa.icp_score": "ICP score",
        "empresa.icp_classificacao": "ICP classificacao",
    },
    "QUALIFICACAO_OPORTUNIDADE": {
        "produto_interesse": "Produto",
        "area_atuacao": "Area de atuacao",
    },
}


class LeadService:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def generate_lead_id(self) -> str:
        result = await self.db.execute(text("SELECT nextval('lead_id_seq')"))
        seq = result.scalar()
        return f"L-{seq:04d}"

    async def create_lead(self, data: LeadCreate, user_id: uuid.UUID) -> Lead:
        emp = await self.db.execute(select(Empresa).where(Empresa.id == data.empresa_id))
        if not emp.scalar_one_or_none():
            raise ValueError("Empresa nao encontrada")

        lead_id = await self.generate_lead_id()
        lead = Lead(
            lead_id=lead_id,
            **data.model_dump(),
        )
        if not lead.responsavel_pre_vendas_id:
            lead.responsavel_pre_vendas_id = user_id
        self.db.add(lead)
        await self.db.flush()

        # Abre histórico inicial em LEAD_INICIAL
        historico = HistoricoEtapaLead(
            lead_id=lead.id,
            etapa="LEAD_INICIAL",
            entrou_em=datetime.utcnow(),
            responsavel_no_periodo_id=lead.responsavel_pre_vendas_id,
        )
        self.db.add(historico)
        await self.db.commit()
        await self.db.refresh(lead)
        return lead

    async def _close_current_history(self, lead_id: uuid.UUID) -> None:
        result = await self.db.execute(
            select(HistoricoEtapaLead)
            .where(HistoricoEtapaLead.lead_id == lead_id)
            .where(HistoricoEtapaLead.saiu_em.is_(None))
        )
        for entry in result.scalars().all():
            entry.saiu_em = datetime.utcnow()

    async def change_stage(
        self,
        lead_id: uuid.UUID,
        nova_etapa: str,
        user_id: uuid.UUID,
        motivo_descarte: str | None = None,
    ) -> Lead:
        # Compat: legacy ChangeStageRequest com nova_etapa="DESCARTADO" delega
        # pro endpoint dedicado descartar_lead.
        if nova_etapa.upper() == "DESCARTADO":
            if not motivo_descarte:
                raise ValueError("motivo_descarte obrigatorio para descartar")
            return await self.descartar_lead(lead_id, motivo_descarte, user_id)

        result = await self.db.execute(select(Lead).where(Lead.id == lead_id))
        lead = result.scalar_one_or_none()
        if not lead:
            raise ValueError("Lead nao encontrado")
        if lead.descartado:
            raise ValueError("Lead descartado nao pode mudar de etapa. Reative primeiro via POST /leads/{id}/reativar")

        if nova_etapa not in ETAPAS_ORDER:
            raise ValueError(f"Etapa invalida: {nova_etapa}")

        await self._close_current_history(lead.id)

        novo_hist = HistoricoEtapaLead(
            lead_id=lead.id,
            etapa=nova_etapa,
            entrou_em=datetime.utcnow(),
            responsavel_no_periodo_id=lead.responsavel_pre_vendas_id,
        )
        self.db.add(novo_hist)

        lead.etapa = nova_etapa
        if nova_etapa == "QUALIFICACAO_OPORTUNIDADE":
            lead.data_qualificacao = datetime.utcnow()

        await self.db.commit()
        await self.db.refresh(lead)
        return lead

    async def descartar_lead(
        self, lead_id: uuid.UUID, motivo: str, user_id: uuid.UUID
    ) -> Lead:
        """SPEC §3.3 - descarte e flag, nao etapa. Fecha historico sem abrir novo."""
        result = await self.db.execute(select(Lead).where(Lead.id == lead_id))
        lead = result.scalar_one_or_none()
        if not lead:
            raise ValueError("Lead nao encontrado")
        if lead.descartado:
            raise ValueError("Lead ja esta descartado")
        if not motivo or not motivo.strip():
            raise ValueError("Motivo do descarte e obrigatorio")

        lead.descartado = True
        lead.data_descarte = datetime.utcnow()
        lead.motivo_descarte = motivo.strip()

        await self._close_current_history(lead.id)

        await self.db.commit()
        await self.db.refresh(lead)
        return lead

    async def reativar_lead(
        self,
        lead_id: uuid.UUID,
        nova_etapa: str,
        status_reativacao: str | None,
        user_id: uuid.UUID,
    ) -> Lead:
        """SPEC §3.3 - reativacao zera flag e abre novo historico."""
        if nova_etapa not in ETAPAS_ORDER:
            raise ValueError(f"Etapa invalida: {nova_etapa}")

        result = await self.db.execute(select(Lead).where(Lead.id == lead_id))
        lead = result.scalar_one_or_none()
        if not lead:
            raise ValueError("Lead nao encontrado")
        if not lead.descartado:
            raise ValueError("Lead nao esta descartado")

        lead.descartado = False
        lead.data_reativacao = datetime.utcnow()
        lead.status_reativacao = status_reativacao
        lead.etapa = nova_etapa

        # Garantia: fecha qualquer historico aberto (descarte ja deveria ter fechado)
        await self._close_current_history(lead.id)

        novo_hist = HistoricoEtapaLead(
            lead_id=lead.id,
            etapa=nova_etapa,
            entrou_em=datetime.utcnow(),
            responsavel_no_periodo_id=lead.responsavel_pre_vendas_id,
        )
        self.db.add(novo_hist)

        await self.db.commit()
        await self.db.refresh(lead)
        return lead

    async def calculate_completude(self, lead: Lead) -> Completude:
        etapa = lead.etapa
        campos = COMPLETUDE_MAP.get(etapa, {})
        filled = []
        missing = []

        for field_path, label in campos.items():
            value = None
            if "." in field_path:
                parts = field_path.split(".")
                obj = lead
                for part in parts:
                    obj = getattr(obj, part, None) if obj else None
                value = obj
            else:
                value = getattr(lead, field_path, None)

            if value and value != 0:
                filled.append(label)
            else:
                missing.append(label)

        total = len(campos)
        pct = (len(filled) / total * 100) if total > 0 else 100

        return Completude(
            etapa=etapa,
            pct=round(pct, 1),
            filled=filled,
            missing=missing,
            total=total,
        )

    async def get_kanban(
        self,
        responsavel_id: uuid.UUID | None = None,
        temperatura: str | None = None,
        search: str | None = None,
        incluir_descartados: bool = False,
    ) -> KanbanResponse:
        query = (
            select(Lead)
            .options(selectinload(Lead.empresa))
            .where(Lead.ativo == True)
        )
        if not incluir_descartados:
            query = query.where(Lead.descartado == False)

        if responsavel_id:
            query = query.where(Lead.responsavel_pre_vendas_id == responsavel_id)
        if temperatura:
            query = query.where(Lead.temperatura == temperatura)
        if search:
            query = query.join(Empresa).where(Empresa.nome_fantasia.ilike(f"%{search}%"))

        result = await self.db.execute(query.order_by(Lead.created_at.desc()))
        leads = result.scalars().all()

        columns = []
        total_leads = 0
        total_valor = 0.0

        for etapa in ETAPAS_ORDER:
            etapa_leads = [l for l in leads if l.etapa == etapa]
            etapa_valor = sum(float(l.valor_estimado) for l in etapa_leads)
            columns.append(KanbanColumn(
                etapa=etapa,
                count=len(etapa_leads),
                total_valor=etapa_valor,
                leads=[LeadResponse.model_validate(l) for l in etapa_leads],
            ))
            total_leads += len(etapa_leads)
            total_valor += etapa_valor

        return KanbanResponse(columns=columns, total_leads=total_leads, total_valor=total_valor)
