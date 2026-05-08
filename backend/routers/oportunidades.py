import uuid

from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy import select, func
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from auth_utils import get_current_user
from database import get_db
from models.oportunidade import Oportunidade
from models.empresa import Empresa
from models.historico_etapa import HistoricoEtapaOportunidade
from schemas.oportunidade import (
    OportunidadeCreate,
    OportunidadeUpdate,
    OportunidadeResponse,
    KanbanResponse,
    ChangeStageRequest,
    DescartarRequest,
    ReativarRequest,
    HistoricoOportunidadeResponse,
)
from services.oportunidade_service import OportunidadeService

router = APIRouter(prefix="/oportunidades", tags=["oportunidades"])


@router.get("/kanban", response_model=KanbanResponse)
async def get_kanban(
    responsavel_comercial_id: uuid.UUID | None = None,
    responsavel_tecnico_id: uuid.UUID | None = None,
    temperatura_comercial: str | None = None,
    search: str | None = None,
    incluir_descartados: bool = False,
    db: AsyncSession = Depends(get_db),
    _user=Depends(get_current_user),
):
    service = OportunidadeService(db)
    return await service.get_kanban(
        responsavel_comercial_id=responsavel_comercial_id,
        responsavel_tecnico_id=responsavel_tecnico_id,
        temperatura_comercial=temperatura_comercial,
        search=search,
        incluir_descartados=incluir_descartados,
    )


@router.get("", response_model=dict)
async def list_oportunidades(
    etapa: str | None = None,
    responsavel_comercial_id: uuid.UUID | None = None,
    responsavel_tecnico_id: uuid.UUID | None = None,
    temperatura_comercial: str | None = None,
    empresa_id: uuid.UUID | None = None,
    search: str | None = None,
    incluir_descartados: bool = False,
    skip: int = Query(0, ge=0),
    limit: int = Query(50, ge=1, le=100),
    db: AsyncSession = Depends(get_db),
    _user=Depends(get_current_user),
):
    query = select(Oportunidade).where(Oportunidade.ativo == True)
    count_query = select(func.count()).select_from(Oportunidade).where(Oportunidade.ativo == True)

    if not incluir_descartados:
        query = query.where(Oportunidade.descartado == False)
        count_query = count_query.where(Oportunidade.descartado == False)

    if etapa:
        query = query.where(Oportunidade.etapa == etapa)
        count_query = count_query.where(Oportunidade.etapa == etapa)
    if responsavel_comercial_id:
        query = query.where(Oportunidade.responsavel_comercial_id == responsavel_comercial_id)
        count_query = count_query.where(Oportunidade.responsavel_comercial_id == responsavel_comercial_id)
    if responsavel_tecnico_id:
        query = query.where(Oportunidade.responsavel_tecnico_id == responsavel_tecnico_id)
        count_query = count_query.where(Oportunidade.responsavel_tecnico_id == responsavel_tecnico_id)
    if temperatura_comercial:
        query = query.where(Oportunidade.temperatura_comercial == temperatura_comercial)
        count_query = count_query.where(Oportunidade.temperatura_comercial == temperatura_comercial)
    if empresa_id:
        query = query.where(Oportunidade.empresa_id == empresa_id)
        count_query = count_query.where(Oportunidade.empresa_id == empresa_id)
    if search:
        query = query.join(Empresa).where(Empresa.nome_fantasia.ilike(f"%{search}%"))
        count_query = count_query.join(Empresa).where(Empresa.nome_fantasia.ilike(f"%{search}%"))

    total = (await db.execute(count_query)).scalar()
    result = await db.execute(query.order_by(Oportunidade.created_at.desc()).offset(skip).limit(limit))
    items = result.scalars().all()

    return {"items": [OportunidadeResponse.model_validate(o) for o in items], "total": total}


@router.post("", response_model=OportunidadeResponse, status_code=201)
async def create_oportunidade(
    data: OportunidadeCreate,
    db: AsyncSession = Depends(get_db),
    current_user=Depends(get_current_user),
):
    service = OportunidadeService(db)
    try:
        opp = await service.create_oportunidade(data, current_user.id)
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
    return OportunidadeResponse.model_validate(opp)


@router.get("/{id}", response_model=OportunidadeResponse)
async def get_oportunidade(
    id: uuid.UUID,
    db: AsyncSession = Depends(get_db),
    _user=Depends(get_current_user),
):
    result = await db.execute(
        select(Oportunidade).options(selectinload(Oportunidade.empresa)).where(Oportunidade.id == id)
    )
    opp = result.scalar_one_or_none()
    if not opp:
        raise HTTPException(status_code=404, detail="Oportunidade nao encontrada")
    return OportunidadeResponse.model_validate(opp)


@router.put("/{id}", response_model=OportunidadeResponse)
async def update_oportunidade(
    id: uuid.UUID,
    data: OportunidadeUpdate,
    db: AsyncSession = Depends(get_db),
    _user=Depends(get_current_user),
):
    result = await db.execute(select(Oportunidade).where(Oportunidade.id == id))
    opp = result.scalar_one_or_none()
    if not opp:
        raise HTTPException(status_code=404, detail="Oportunidade nao encontrada")

    update_data = data.model_dump(exclude_unset=True)
    for key, value in update_data.items():
        setattr(opp, key, value)

    await db.commit()
    await db.refresh(opp)
    return OportunidadeResponse.model_validate(opp)


@router.delete("/{id}", status_code=204)
async def delete_oportunidade(
    id: uuid.UUID,
    db: AsyncSession = Depends(get_db),
    _user=Depends(get_current_user),
):
    result = await db.execute(select(Oportunidade).where(Oportunidade.id == id))
    opp = result.scalar_one_or_none()
    if not opp:
        raise HTTPException(status_code=404, detail="Oportunidade nao encontrada")
    opp.ativo = False
    await db.commit()


@router.post("/{id}/change-stage", response_model=OportunidadeResponse)
async def change_stage(
    id: uuid.UUID,
    data: ChangeStageRequest,
    db: AsyncSession = Depends(get_db),
    current_user=Depends(get_current_user),
):
    service = OportunidadeService(db)
    try:
        opp = await service.change_stage(id, data.nova_etapa, current_user.id)
    except ValueError as e:
        raise HTTPException(status_code=422, detail=str(e))
    return OportunidadeResponse.model_validate(opp)


@router.post("/{id}/descartar", response_model=OportunidadeResponse)
async def descartar_oportunidade(
    id: uuid.UUID,
    data: DescartarRequest,
    db: AsyncSession = Depends(get_db),
    current_user=Depends(get_current_user),
):
    service = OportunidadeService(db)
    try:
        opp = await service.descartar_oportunidade(id, data.motivo, current_user.id)
    except ValueError as e:
        raise HTTPException(status_code=422, detail=str(e))
    return OportunidadeResponse.model_validate(opp)


@router.post("/{id}/reativar", response_model=OportunidadeResponse)
async def reativar_oportunidade(
    id: uuid.UUID,
    data: ReativarRequest,
    db: AsyncSession = Depends(get_db),
    current_user=Depends(get_current_user),
):
    service = OportunidadeService(db)
    try:
        opp = await service.reativar_oportunidade(id, data.nova_etapa, data.status_reativacao, current_user.id)
    except ValueError as e:
        raise HTTPException(status_code=422, detail=str(e))
    return OportunidadeResponse.model_validate(opp)


@router.get("/{id}/historico", response_model=list[HistoricoOportunidadeResponse])
async def get_historico(
    id: uuid.UUID,
    db: AsyncSession = Depends(get_db),
    _user=Depends(get_current_user),
):
    result = await db.execute(
        select(HistoricoEtapaOportunidade)
        .where(HistoricoEtapaOportunidade.oportunidade_id == id)
        .order_by(HistoricoEtapaOportunidade.entrou_em.desc())
    )
    items = result.scalars().all()
    return [HistoricoOportunidadeResponse.model_validate(h) for h in items]
