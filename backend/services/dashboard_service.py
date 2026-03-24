from datetime import datetime, timedelta

from sqlalchemy import select, func, and_
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from models.lead import Lead
from models.atividade import Atividade
from models.origem import Origem
from sla_config import SLA_RULES


class DashboardService:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def get_kpis(self) -> dict:
        now = datetime.utcnow()
        month_start = now.replace(day=1, hour=0, minute=0, second=0, microsecond=0)

        # Leads this month
        new_leads = await self.db.execute(
            select(func.count()).select_from(Lead).where(Lead.data_entrada >= month_start)
        )

        # Leads by stage
        by_stage = await self.db.execute(
            select(Lead.etapa, func.count()).group_by(Lead.etapa)
        )

        # Pipeline value
        pipeline_value = await self.db.execute(
            select(func.sum(Lead.valor_estimado)).where(Lead.etapa != "descartado")
        )

        # By temperature
        by_temp = await self.db.execute(
            select(Lead.temperatura, func.count())
            .where(Lead.etapa != "descartado")
            .group_by(Lead.temperatura)
        )

        # Conversion rate
        total_leads = await self.db.execute(select(func.count()).select_from(Lead))
        qualified = await self.db.execute(
            select(func.count()).select_from(Lead).where(Lead.etapa == "qualificado")
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

    async def get_sla_alerts(self) -> list[dict]:
        alerts = []
        now = datetime.utcnow()

        result = await self.db.execute(
            select(Lead)
            .options(selectinload(Lead.origem), selectinload(Lead.empresa))
            .where(Lead.etapa.notin_(["qualificado", "descartado"]))
        )
        leads = result.scalars().all()

        for lead in leads:
            etapa = lead.etapa
            origem_tipo = lead.origem.tipo if lead.origem else None
            origem_sub = lead.origem.sub_tipo if lead.origem else None

            # Find matching SLA rule
            sla_days = None
            for (rule_etapa, rule_tipo, rule_sub), days in SLA_RULES.items():
                if rule_etapa == etapa:
                    if rule_tipo is None or rule_tipo == origem_tipo:
                        if rule_sub is None or rule_sub == origem_sub:
                            sla_days = days
                            break

            if sla_days is None:
                continue

            days_in_stage = (now - lead.data_entrada).days
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

        # Activities today
        today_count = await self.db.execute(
            select(func.count()).select_from(Atividade).where(
                and_(Atividade.data_prevista >= today_start, Atividade.data_prevista < today_start + timedelta(days=1), Atividade.concluida == False)
            )
        )

        # Overdue activities
        overdue_count = await self.db.execute(
            select(func.count()).select_from(Atividade).where(
                and_(Atividade.data_prevista < today_start, Atividade.concluida == False)
            )
        )

        # This week
        week_count = await self.db.execute(
            select(func.count()).select_from(Atividade).where(
                and_(Atividade.data_prevista >= today_start, Atividade.data_prevista < week_end, Atividade.concluida == False)
            )
        )

        # Leads without activity
        leads_no_activity = await self.db.execute(
            select(func.count()).select_from(Lead).where(
                and_(
                    Lead.etapa.notin_(["qualificado", "descartado"]),
                    ~Lead.id.in_(select(Atividade.lead_id).distinct())
                )
            )
        )

        # Leads without next activity
        leads_no_next = await self.db.execute(
            select(func.count()).select_from(Lead).where(
                and_(
                    Lead.etapa.notin_(["qualificado", "descartado"]),
                    Lead.data_prox_atividade == None,
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
