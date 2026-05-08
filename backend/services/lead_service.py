import uuid
from datetime import datetime

from sqlalchemy import select, func, text
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from models.lead import Lead
from models.empresa import Empresa
from models.historico_etapa import HistoricoEtapa
from schemas.lead import LeadCreate, KanbanResponse, KanbanColumn, LeadResponse, Completude

ETAPAS_ORDER = ["prospeccao", "primeiro_contato", "qualificacao", "qualificado", "descartado"]

COMPLETUDE_MAP = {
    "prospeccao": {
        "empresa.nome_fantasia": "Nome da empresa",
        "origem_id": "Origem",
        "empresa.cnpj": "CNPJ",
        "empresa.telefone_fixo": "Telefone fixo",
        "contato_principal.nome": "Nome do contato",
        "contato_principal.whatsapp": "Telefone/WhatsApp",
        "contato_principal.email": "E-mail",
    },
    "primeiro_contato": {
        "produto_interesse": "Produto",
        "area_atuacao": "Área de atuação",
    },
    "qualificacao": {
        "tipo_entrega": "Tipo de entrega",
        "lead_score": "Opportunity Score",
    },
    "descartado": {
        "motivo_descarte": "Motivo de descarte",
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
            raise ValueError("Empresa não encontrada")

        lead_id = await self.generate_lead_id()
        lead = Lead(
            lead_id=lead_id,
            **data.model_dump(),
        )
        if not lead.responsavel_id:
            lead.responsavel_id = user_id
        self.db.add(lead)
        await self.db.flush()

        # Create initial history entry
        historico = HistoricoEtapa(
            lead_id=lead.id,
            etapa_anterior=None,
            etapa_nova="prospeccao",
            usuario_id=user_id,
        )
        self.db.add(historico)
        await self.db.commit()
        await self.db.refresh(lead)
        return lead

    async def change_stage(
        self, lead_id: uuid.UUID, nova_etapa: str, user_id: uuid.UUID, motivo_descarte: str | None = None
    ) -> Lead:
        result = await self.db.execute(select(Lead).where(Lead.id == lead_id))
        lead = result.scalar_one_or_none()
        if not lead:
            raise ValueError("Lead não encontrado")

        if nova_etapa not in ETAPAS_ORDER:
            raise ValueError(f"Etapa inválida: {nova_etapa}")

        etapa_anterior = lead.etapa

        # Calculate time in previous stage
        last_hist = await self.db.execute(
            select(HistoricoEtapa)
            .where(HistoricoEtapa.lead_id == lead.id)
            .order_by(HistoricoEtapa.created_at.desc())
            .limit(1)
        )
        last_entry = last_hist.scalar_one_or_none()
        tempo_segundos = None
        if last_entry:
            delta = datetime.utcnow() - last_entry.created_at
            tempo_segundos = int(delta.total_seconds())

        # Create history
        historico = HistoricoEtapa(
            lead_id=lead.id,
            etapa_anterior=etapa_anterior,
            etapa_nova=nova_etapa,
            tempo_na_etapa_segundos=tempo_segundos,
            usuario_id=user_id,
        )
        self.db.add(historico)

        # Update lead
        lead.etapa = nova_etapa
        if nova_etapa == "qualificado":
            lead.data_qualificacao = datetime.utcnow()
        if nova_etapa == "descartado" and motivo_descarte:
            lead.motivo_descarte = motivo_descarte

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
    ) -> KanbanResponse:
        query = select(Lead).options(selectinload(Lead.empresa)).where(Lead.ativo == True)

        if responsavel_id:
            query = query.where(Lead.responsavel_id == responsavel_id)
        if temperatura:
            query = query.where(Lead.temperatura == temperatura)
        if search:
            from models.empresa import Empresa
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
