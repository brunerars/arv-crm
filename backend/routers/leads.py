import uuid

from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy import select, func
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from auth_utils import get_current_user
from database import get_db
from models.lead import Lead
from models.historico_etapa import HistoricoEtapaLead
from schemas.lead import (
    LeadCreate, LeadUpdate, LeadResponse, LeadDetail,
    KanbanResponse, KanbanColumn,
    ChangeStageRequest, DescartarRequest, ReativarRequest,
    Completude, HistoricoResponse,
)
from schemas.empresa import EmpresaResponse
from schemas.contato import ContatoResponse
from services.lead_service import LeadService

router = APIRouter(prefix="/leads", tags=["leads"])


@router.get("/kanban", response_model=KanbanResponse)
async def get_kanban(
    responsavel_id: uuid.UUID | None = None,
    temperatura: str | None = None,
    search: str | None = None,
    incluir_descartados: bool = False,
    db: AsyncSession = Depends(get_db),
    _user=Depends(get_current_user),
):
    service = LeadService(db)
    return await service.get_kanban(
        responsavel_id=responsavel_id,
        temperatura=temperatura,
        search=search,
        incluir_descartados=incluir_descartados,
    )


@router.get("/descartados", response_model=dict)
async def list_descartados(
    responsavel_id: uuid.UUID | None = None,
    search: str | None = None,
    skip: int = Query(0, ge=0),
    limit: int = Query(50, ge=1, le=100),
    db: AsyncSession = Depends(get_db),
    _user=Depends(get_current_user),
):
    query = select(Lead).where(Lead.ativo == True).where(Lead.descartado == True)
    count_query = select(func.count()).select_from(Lead).where(Lead.ativo == True).where(Lead.descartado == True)

    if responsavel_id:
        query = query.where(Lead.responsavel_pre_vendas_id == responsavel_id)
        count_query = count_query.where(Lead.responsavel_pre_vendas_id == responsavel_id)
    if search:
        from models.empresa import Empresa
        query = query.join(Empresa).where(Empresa.nome_fantasia.ilike(f"%{search}%"))
        count_query = count_query.join(Empresa).where(Empresa.nome_fantasia.ilike(f"%{search}%"))

    total = (await db.execute(count_query)).scalar()
    result = await db.execute(query.order_by(Lead.data_descarte.desc()).offset(skip).limit(limit))
    items = result.scalars().all()

    return {"items": [LeadResponse.model_validate(l) for l in items], "total": total}


@router.get("", response_model=dict)
async def list_leads(
    etapa: str | None = None,
    temperatura: str | None = None,
    responsavel_id: uuid.UUID | None = None,
    search: str | None = None,
    incluir_descartados: bool = False,
    skip: int = Query(0, ge=0),
    limit: int = Query(50, ge=1, le=100),
    db: AsyncSession = Depends(get_db),
    _user=Depends(get_current_user),
):
    query = select(Lead).where(Lead.ativo == True)
    count_query = select(func.count()).select_from(Lead).where(Lead.ativo == True)

    if not incluir_descartados:
        query = query.where(Lead.descartado == False)
        count_query = count_query.where(Lead.descartado == False)

    if etapa:
        query = query.where(Lead.etapa == etapa)
        count_query = count_query.where(Lead.etapa == etapa)
    if temperatura:
        query = query.where(Lead.temperatura == temperatura)
        count_query = count_query.where(Lead.temperatura == temperatura)
    if responsavel_id:
        query = query.where(Lead.responsavel_pre_vendas_id == responsavel_id)
        count_query = count_query.where(Lead.responsavel_pre_vendas_id == responsavel_id)
    if search:
        from models.empresa import Empresa
        query = query.join(Empresa).where(Empresa.nome_fantasia.ilike(f"%{search}%"))
        count_query = count_query.join(Empresa).where(Empresa.nome_fantasia.ilike(f"%{search}%"))

    total = (await db.execute(count_query)).scalar()
    result = await db.execute(query.order_by(Lead.created_at.desc()).offset(skip).limit(limit))
    items = result.scalars().all()

    return {"items": [LeadResponse.model_validate(l) for l in items], "total": total}


@router.post("", response_model=LeadResponse, status_code=201)
async def create_lead(
    data: LeadCreate,
    db: AsyncSession = Depends(get_db),
    current_user=Depends(get_current_user),
):
    service = LeadService(db)
    try:
        lead = await service.create_lead(data, current_user.id)
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
    return LeadResponse.model_validate(lead)


@router.get("/{id}", response_model=LeadDetail)
async def get_lead(
    id: uuid.UUID,
    db: AsyncSession = Depends(get_db),
    _user=Depends(get_current_user),
):
    result = await db.execute(
        select(Lead)
        .options(selectinload(Lead.empresa), selectinload(Lead.contato_principal))
        .where(Lead.id == id)
    )
    lead = result.scalar_one_or_none()
    if not lead:
        raise HTTPException(status_code=404, detail="Lead não encontrado")

    service = LeadService(db)
    completude = await service.calculate_completude(lead)

    detail = LeadDetail.model_validate(lead)
    detail.empresa = EmpresaResponse.model_validate(lead.empresa) if lead.empresa else None
    detail.contato_principal = ContatoResponse.model_validate(lead.contato_principal) if lead.contato_principal else None
    detail.completude = completude.model_dump()
    return detail


@router.put("/{id}", response_model=LeadResponse)
async def update_lead(
    id: uuid.UUID,
    data: LeadUpdate,
    db: AsyncSession = Depends(get_db),
    _user=Depends(get_current_user),
):
    result = await db.execute(select(Lead).where(Lead.id == id))
    lead = result.scalar_one_or_none()
    if not lead:
        raise HTTPException(status_code=404, detail="Lead não encontrado")

    update_data = data.model_dump(exclude_unset=True)
    for key, value in update_data.items():
        setattr(lead, key, value)

    await db.commit()
    await db.refresh(lead)
    return LeadResponse.model_validate(lead)


@router.delete("/{id}", status_code=204)
async def delete_lead(
    id: uuid.UUID,
    db: AsyncSession = Depends(get_db),
    _user=Depends(get_current_user),
):
    result = await db.execute(select(Lead).where(Lead.id == id))
    lead = result.scalar_one_or_none()
    if not lead:
        raise HTTPException(status_code=404, detail="Lead não encontrado")
    lead.ativo = False
    await db.commit()


@router.post("/{id}/change-stage", response_model=LeadResponse)
async def change_stage(
    id: uuid.UUID,
    data: ChangeStageRequest,
    db: AsyncSession = Depends(get_db),
    current_user=Depends(get_current_user),
):
    service = LeadService(db)
    try:
        lead = await service.change_stage(id, data.nova_etapa, current_user.id, data.motivo_descarte)
    except ValueError as e:
        raise HTTPException(status_code=422, detail=str(e))
    return LeadResponse.model_validate(lead)


@router.post("/{id}/descartar", response_model=LeadResponse)
async def descartar_lead(
    id: uuid.UUID,
    data: DescartarRequest,
    db: AsyncSession = Depends(get_db),
    current_user=Depends(get_current_user),
):
    service = LeadService(db)
    try:
        lead = await service.descartar_lead(id, data.motivo, current_user.id)
    except ValueError as e:
        raise HTTPException(status_code=422, detail=str(e))
    return LeadResponse.model_validate(lead)


@router.post("/{id}/reativar", response_model=LeadResponse)
async def reativar_lead(
    id: uuid.UUID,
    data: ReativarRequest,
    db: AsyncSession = Depends(get_db),
    current_user=Depends(get_current_user),
):
    service = LeadService(db)
    try:
        lead = await service.reativar_lead(id, data.nova_etapa, data.status_reativacao, current_user.id)
    except ValueError as e:
        raise HTTPException(status_code=422, detail=str(e))
    return LeadResponse.model_validate(lead)


@router.get("/{id}/completude", response_model=Completude)
async def get_completude(
    id: uuid.UUID,
    db: AsyncSession = Depends(get_db),
    _user=Depends(get_current_user),
):
    result = await db.execute(
        select(Lead).options(selectinload(Lead.empresa), selectinload(Lead.contato_principal)).where(Lead.id == id)
    )
    lead = result.scalar_one_or_none()
    if not lead:
        raise HTTPException(status_code=404, detail="Lead não encontrado")

    service = LeadService(db)
    return await service.calculate_completude(lead)


@router.get("/{id}/historico", response_model=list[HistoricoResponse])
async def get_historico(
    id: uuid.UUID,
    db: AsyncSession = Depends(get_db),
    _user=Depends(get_current_user),
):
    result = await db.execute(
        select(HistoricoEtapaLead)
        .where(HistoricoEtapaLead.lead_id == id)
        .order_by(HistoricoEtapaLead.entrou_em.desc())
    )
    items = result.scalars().all()
    return [HistoricoResponse.model_validate(h) for h in items]


@router.post("/{id}/calculate-score", response_model=LeadResponse)
async def calculate_score(
    id: uuid.UUID,
    db: AsyncSession = Depends(get_db),
    _user=Depends(get_current_user),
):
    from services.scoring_service import ScoringService
    result = await db.execute(select(Lead).options(selectinload(Lead.empresa)).where(Lead.id == id))
    lead = result.scalar_one_or_none()
    if not lead:
        raise HTTPException(status_code=404, detail="Lead não encontrado")

    scoring = ScoringService(db)
    lead = await scoring.calculate_score(lead)
    return LeadResponse.model_validate(lead)
