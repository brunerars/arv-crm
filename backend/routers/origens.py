from fastapi import APIRouter, Depends
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from auth_utils import get_current_user
from database import get_db
from models.origem import Origem
from schemas.origem import OrigemResponse

router = APIRouter(prefix="/origens", tags=["origens"])


@router.get("", response_model=list[OrigemResponse])
async def list_origens(
    db: AsyncSession = Depends(get_db),
    _user=Depends(get_current_user),
):
    result = await db.execute(select(Origem).order_by(Origem.tipo, Origem.sub_tipo))
    items = result.scalars().all()
    return [OrigemResponse.model_validate(o) for o in items]
