import uuid

from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy import select, func, or_
from sqlalchemy.ext.asyncio import AsyncSession

from auth_utils import get_current_user
from database import get_db
from models.empresa import Empresa
from schemas.empresa import EmpresaCreate, EmpresaUpdate, EmpresaResponse, EmpresaList

router = APIRouter(prefix="/empresas", tags=["empresas"])


@router.get("", response_model=EmpresaList)
async def list_empresas(
    search: str | None = None,
    status_conta: str | None = None,
    responsavel_id: uuid.UUID | None = None,
    segmento: str | None = None,
    incluir_inativos: bool = False,
    skip: int = Query(0, ge=0),
    limit: int = Query(50, ge=1, le=100),
    db: AsyncSession = Depends(get_db),
    _user=Depends(get_current_user),
):
    query = select(Empresa)
    count_query = select(func.count()).select_from(Empresa)

    if not incluir_inativos:
        query = query.where(Empresa.ativo == True)
        count_query = count_query.where(Empresa.ativo == True)

    if search:
        search_filter = or_(
            Empresa.nome_fantasia.ilike(f"%{search}%"),
            Empresa.razao_social.ilike(f"%{search}%"),
            Empresa.cnpj.ilike(f"%{search}%"),
        )
        query = query.where(search_filter)
        count_query = count_query.where(search_filter)

    if status_conta:
        query = query.where(Empresa.status_conta == status_conta)
        count_query = count_query.where(Empresa.status_conta == status_conta)

    if responsavel_id:
        query = query.where(Empresa.responsavel_id == responsavel_id)
        count_query = count_query.where(Empresa.responsavel_id == responsavel_id)

    if segmento:
        query = query.where(Empresa.segmento == segmento)
        count_query = count_query.where(Empresa.segmento == segmento)

    total = (await db.execute(count_query)).scalar()
    result = await db.execute(query.order_by(Empresa.created_at.desc()).offset(skip).limit(limit))
    items = result.scalars().all()

    return EmpresaList(items=[EmpresaResponse.model_validate(e) for e in items], total=total)


@router.post("", response_model=EmpresaResponse, status_code=201)
async def create_empresa(
    data: EmpresaCreate,
    db: AsyncSession = Depends(get_db),
    _user=Depends(get_current_user),
):
    empresa = Empresa(**data.model_dump())
    db.add(empresa)
    await db.commit()
    await db.refresh(empresa)
    return EmpresaResponse.model_validate(empresa)


@router.get("/{id}", response_model=EmpresaResponse)
async def get_empresa(
    id: uuid.UUID,
    db: AsyncSession = Depends(get_db),
    _user=Depends(get_current_user),
):
    result = await db.execute(select(Empresa).where(Empresa.id == id))
    empresa = result.scalar_one_or_none()
    if not empresa:
        raise HTTPException(status_code=404, detail="Empresa não encontrada")
    return EmpresaResponse.model_validate(empresa)


@router.put("/{id}", response_model=EmpresaResponse)
async def update_empresa(
    id: uuid.UUID,
    data: EmpresaUpdate,
    db: AsyncSession = Depends(get_db),
    _user=Depends(get_current_user),
):
    result = await db.execute(select(Empresa).where(Empresa.id == id))
    empresa = result.scalar_one_or_none()
    if not empresa:
        raise HTTPException(status_code=404, detail="Empresa não encontrada")

    update_data = data.model_dump(exclude_unset=True)
    for key, value in update_data.items():
        setattr(empresa, key, value)

    await db.commit()
    await db.refresh(empresa)
    return EmpresaResponse.model_validate(empresa)


@router.delete("/{id}", status_code=204)
async def delete_empresa(
    id: uuid.UUID,
    db: AsyncSession = Depends(get_db),
    _user=Depends(get_current_user),
):
    result = await db.execute(select(Empresa).where(Empresa.id == id))
    empresa = result.scalar_one_or_none()
    if not empresa:
        raise HTTPException(status_code=404, detail="Empresa não encontrada")
    empresa.ativo = False
    await db.commit()


@router.post("/{id}/enrich-cnpj", response_model=EmpresaResponse)
async def enrich_cnpj(
    id: uuid.UUID,
    db: AsyncSession = Depends(get_db),
    _user=Depends(get_current_user),
):
    from services.cnpj_service import enrich_empresa_cnpj
    result = await db.execute(select(Empresa).where(Empresa.id == id))
    empresa = result.scalar_one_or_none()
    if not empresa:
        raise HTTPException(status_code=404, detail="Empresa não encontrada")
    if not empresa.cnpj:
        raise HTTPException(status_code=400, detail="Empresa sem CNPJ cadastrado")

    empresa = await enrich_empresa_cnpj(empresa, db)
    return EmpresaResponse.model_validate(empresa)
