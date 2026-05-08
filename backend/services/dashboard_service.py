"""Dashboard antigo - mantido funcional ate Macro C1-C3 reescrever
para os 3 dashboards Fase 1A (Saude do Funil, Tracao PV/V, Check-in).
"""
from datetime import datetime, timedelta

from sqlalchemy import select, func, and_
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from models.lead import Lead
from models.atividade import Atividade
from models.historico_etapa import HistoricoEtapaLead
from sla_config import SLA_RULES


class DashboardService:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def get_kpis(self) -> dict:
        now = datetime.utcnow()
        month_start = now.replace(day=1, hour=0, minute=0, second=0, microsecond=0)

        new_leads = await self.db.execute(
            select(func.count())
            .select_from(Lead)
            .where(Lead.data_entrada_pre_vendas >= month_start)
        )

        by_stage = await self.db.execute(
            select(Lead.etapa, func.count())
            .where(Lead.descartado == False)
            .group_by(Lead.etapa)
        )

        pipeline_value = await self.db.execute(
            select(func.sum(Lead.valor_estimado)).where(Lead.descartado == False)
        )

        by_temp = await self.db.execute(
            select(Lead.temperatura, func.count())
            .where(Lead.descartado == False)
            .group_by(Lead.temperatura)
        )

        total_leads = await self.db.execute(select(func.count()).select_from(Lead))
        qualified = await self.db.execute(
            select(func.count())
            .select_from(Lead)
            .where(Lead.etapa == "QUALIFICACAO_OPORTUNIDADE")
        )

        total_count = total_leads.scalar() or 0
        qualified_count = qualified.scalar() or 0
        conversion_rate = round((qualified_count / total_count * 100) if total_count > 0 else 0, 1)

        return {
            "leads_novos_mes": new_leads.scalar() or 0,
            "leads_por_etapa": dict(by_stage.all()),
            "valor_pipeline": float(pipeline_value.scalar() or 0),
            "taxa_conversao": conversion_rate,
            "por_temperatura": dict(by_temp.all()),
        }

    async def _entrou_em_etapa_atual(self, lead_id) -> datetime | None:
        result = await self.db.execute(
            select(HistoricoEtapaLead.entrou_em)
            .where(HistoricoEtapaLead.lead_id == lead_id)
            .where(HistoricoEtapaLead.saiu_em.is_(None))
            .order_by(HistoricoEtapaLead.entrou_em.desc())
            .limit(1)
        )
        return result.scalar()

    async def get_sla_alerts(self) -> list[dict]:
        alerts = []
        now = datetime.utcnow()

        result = await self.db.execute(
            select(Lead)
            .options(selectinload(Lead.origem), selectinload(Lead.empresa))
            .where(Lead.descartado == False)
            .where(Lead.ativo == True)
        )
        leads = result.scalars().all()

        for lead in leads:
            etapa = lead.etapa
            origem_tipo = lead.origem.tipo if lead.origem else None
            origem_sub = lead.origem.sub_tipo if lead.origem else None

            sla_days = None
            for (rule_etapa, rule_tipo, rule_sub), days in SLA_RULES.items():
                if rule_etapa == etapa:
                    if rule_tipo is None or rule_tipo == origem_tipo:
                        if rule_sub is None or rule_sub == origem_sub:
                            sla_days = days
                            break

            if sla_days is None:
                continue

            entrou_em = await self._entrou_em_etapa_atual(lead.id)
            if entrou_em is None:
                continue

            days_in_stage = (now - entrou_em).days
            if days_in_stage > sla_days:
                overdue_days = days_in_stage - sla_days
                severity = "critical" if overdue_days > sla_days else "warning"
                alerts.append({
                    "lead_id": str(lead.id),
                    "lead_display_id": lead.lead_id,
                    "empresa": lead.empresa.nome_fantasia if lead.empresa else "N/A",
                    "etapa": etapa,
                    "dias_na_etapa": days_in_stage,
                    "sla_dias": sla_days,
                    "overdue_dias": overdue_days,
                    "severity": severity,
                })

        alerts.sort(key=lambda x: x["overdue_dias"], reverse=True)
        return alerts

    async def get_activity_summary(self) -> dict:
        now = datetime.utcnow()
        today_start = now.replace(hour=0, minute=0, second=0, microsecond=0)
        week_end = today_start + timedelta(days=7)

        nao_concluida = Atividade.status != "realizada"

        today_count = await self.db.execute(
            select(func.count())
            .select_from(Atividade)
            .where(
                and_(
                    Atividade.data_prevista >= today_start,
                    Atividade.data_prevista < today_start + timedelta(days=1),
                    nao_concluida,
                )
            )
        )

        overdue_count = await self.db.execute(
            select(func.count())
            .select_from(Atividade)
            .where(and_(Atividade.data_prevista < today_start, nao_concluida))
        )

        week_count = await self.db.execute(
            select(func.count())
            .select_from(Atividade)
            .where(
                and_(
                    Atividade.data_prevista >= today_start,
                    Atividade.data_prevista < week_end,
                    nao_concluida,
                )
            )
        )

        leads_no_activity = await self.db.execute(
            select(func.count())
            .select_from(Lead)
            .where(
                and_(
                    Lead.descartado == False,
                    ~Lead.id.in_(select(Atividade.lead_id).where(Atividade.lead_id.is_not(None)).distinct()),
                )
            )
        )

        leads_no_next = await self.db.execute(
            select(func.count())
            .select_from(Lead)
            .where(
                and_(
                    Lead.descartado == False,
                    Lead.data_prox_atividade.is_(None),
                )
            )
        )

        return {
            "atividades_hoje": today_count.scalar() or 0,
            "atividades_atrasadas": overdue_count.scalar() or 0,
            "atividades_semana": week_count.scalar() or 0,
            "leads_sem_atividade": leads_no_activity.scalar() or 0,
            "leads_sem_prox_atividade": leads_no_next.scalar() or 0,
        }
