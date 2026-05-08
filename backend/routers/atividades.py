import uuid
from datetime import datetime

from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy import select, func
from sqlalchemy.ext.asyncio import AsyncSession

from auth_utils import get_current_user
from database import get_db
from models.atividade import Atividade
from schemas.atividade import AtividadeCreate, AtividadeUpdate, AtividadeResponse, AtividadeList

router = APIRouter(prefix="/atividades", tags=["atividades"])


@router.get("", response_model=AtividadeList)
async def list_atividades(
    lead_id: uuid.UUID | None = None,
    oportunidade_id: uuid.UUID | None = None,
    empresa_id: uuid.UUID | None = None,
    status: str | None = None,
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
    if oportunidade_id:
        query = query.where(Atividade.oportunidade_id == oportunidade_id)
        count_query = count_query.where(Atividade.oportunidade_id == oportunidade_id)
    if empresa_id:
        query = query.where(Atividade.empresa_id == empresa_id)
        count_query = count_query.where(Atividade.empresa_id == empresa_id)
    if status:
        query = query.where(Atividade.status == status)
        count_query = count_query.where(Atividade.status == status)

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
    atividade = Atividade(**data.model_dump(), criada_por_id=current_user.id)
    if not atividade.responsavel_id:
        atividade.responsavel_id = current_user.id
    db.add(atividade)
    await db.commit()
    await db.refresh(atividade)
    return AtividadeResponse.model_validate(atividade)


@router.put("/{id}", response_model=AtividadeResponse)
async def update_atividade(
    id: uuid.UUID,
    data: AtividadeUpdate,
    db: AsyncSession = Depends(get_db),
    _user=Depends(get_current_user),
):
    result = await db.execute(select(Atividade).where(Atividade.id == id))
    atividade = result.scalar_one_or_none()
    if not atividade:
        raise HTTPException(status_code=404, detail="Atividade nao encontrada")

    update_data = data.model_dump(exclude_unset=True)
    for key, value in update_data.items():
        setattr(atividade, key, value)

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
        raise HTTPException(status_code=404, detail="Atividade nao encontrada")

    atividade.status = "realizada"
    atividade.data_realizacao = datetime.utcnow()
    await db.commit()
    await db.refresh(atividade)
    return AtividadeResponse.model_validate(atividade)
