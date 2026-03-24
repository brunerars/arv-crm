from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from auth_utils import get_current_user
from database import get_db
from services.dashboard_service import DashboardService

router = APIRouter(prefix="/dashboard", tags=["dashboard"])


@router.get("")
async def get_dashboard(
    db: AsyncSession = Depends(get_db),
    _user=Depends(get_current_user),
):
    service = DashboardService(db)
    kpis = await service.get_kpis()
    sla_alerts = await service.get_sla_alerts()
    activity_summary = await service.get_activity_summary()
    return {
        "kpis": kpis,
        "sla_alerts": sla_alerts,
        "activity_summary": activity_summary,
    }
