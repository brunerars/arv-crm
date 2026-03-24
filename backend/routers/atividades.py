import uuid
from datetime import datetime

from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy import select, func
from sqlalchemy.ext.asyncio import AsyncSession

from auth_utils import get_current_user
from database import get_db
from models.atividade import Atividade
from schemas.atividade import AtividadeCreate, AtividadeResponse, AtividadeList

router = APIRouter(prefix="/atividades", tags=["atividades"])


@router.get("", response_model=AtividadeList)
async def list_atividades(
    lead_id: uuid.UUID | None = None,
    concluida: bool | None = None,
    skip: int = Query(0, ge=0),
    limit: int = Query(50, ge=1, le=100),
    db: AsyncSession = Depends(get_db),
    _user=Depends(get_current_user),
):
    query = select(Atividade)
    count_query = select(func.count()).select_from(Atividade)

    if lead_id:
        query = query.where(Atividade.lead_id == lead_id)
        count_query = count_query.where(Atividade.lead_id == lead_id)
    if concluida is not None:
        query = query.where(Atividade.concluida == concluida)
        count_query = count_query.where(Atividade.concluida == concluida)

    total = (await db.execute(count_query)).scalar()
    result = await db.execute(query.order_by(Atividade.created_at.desc()).offset(skip).limit(limit))
    items = result.scalars().all()

    return AtividadeList(items=[AtividadeResponse.model_validate(a) for a in items], total=total)


@router.post("", response_model=AtividadeResponse, status_code=201)
async def create_atividade(
    data: AtividadeCreate,
    db: AsyncSession = Depends(get_db),
    current_user=Depends(get_current_user),
):
    atividade = Atividade(**data.model_dump())
    if not atividade.responsavel_id:
        atividade.responsavel_id = current_user.id
    db.add(atividade)
    await db.commit()
    await db.refresh(atividade)
    return AtividadeResponse.model_validate(atividade)


@router.post("/{id}/complete", response_model=AtividadeResponse)
async def complete_atividade(
    id: uuid.UUID,
    db: AsyncSession = Depends(get_db),
    _user=Depends(get_current_user),
):
    result = await db.execute(select(Atividade).where(Atividade.id == id))
    atividade = result.scalar_one_or_none()
    if not atividade:
        raise HTTPException(status_code=404, detail="Atividade não encontrada")

    atividade.concluida = True
    atividade.data_conclusao = datetime.utcnow()
    await db.commit()
    await db.refresh(atividade)
    return AtividadeResponse.model_validate(atividade)
