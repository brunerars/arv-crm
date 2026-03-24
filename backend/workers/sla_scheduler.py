import json
import logging
from datetime import datetime

import redis.asyncio as aioredis
from sqlalchemy import select
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession
from sqlalchemy.orm import selectinload

from config import settings
from models.lead import Lead
from sla_config import SLA_RULES

logger = logging.getLogger(__name__)

_redis = None

def _get_redis():
    global _redis
    if _redis is None:
        _redis = aioredis.from_url(settings.REDIS_URL, decode_responses=True)
    return _redis


async def check_sla_violations():
    logger.info("Checking SLA violations...")
    engine = create_async_engine(settings.DATABASE_URL)
    session_factory = async_sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)

    async with session_factory() as db:
        now = datetime.utcnow()
        result = await db.execute(
            select(Lead)
            .options(selectinload(Lead.origem), selectinload(Lead.empresa))
            .where(Lead.etapa.notin_(["qualificado", "descartado"]))
        )
        leads = result.scalars().all()

        violations = []
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

            days_in_stage = (now - lead.data_entrada).days
            if days_in_stage > sla_days:
                violations.append({
                    "lead_id": str(lead.id),
                    "lead_display_id": lead.lead_id,
                    "empresa": lead.empresa.nome_fantasia if lead.empresa else "N/A",
                    "etapa": etapa,
                    "dias_na_etapa": days_in_stage,
                    "sla_dias": sla_days,
                })

        date_key = now.strftime("%Y-%m-%d")
        await _get_redis().set(f"sla:violations:{date_key}", json.dumps(violations), ex=86400)
        logger.info(f"Found {len(violations)} SLA violations")

    await engine.dispose()
