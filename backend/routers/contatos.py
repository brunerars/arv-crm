import uuid

from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy import select, func
from sqlalchemy.ext.asyncio import AsyncSession

from auth_utils import get_current_user
from database import get_db
from models.contato import Contato
from models.empresa import Empresa
from schemas.contato import ContatoCreate, ContatoUpdate, ContatoResponse, ContatoList

router = APIRouter(prefix="/contatos", tags=["contatos"])


@router.get("", response_model=ContatoList)
async def list_contatos(
    empresa_id: uuid.UUID | None = None,
    search: str | None = None,
    skip: int = Query(0, ge=0),
    limit: int = Query(50, ge=1, le=100),
    db: AsyncSession = Depends(get_db),
    _user=Depends(get_current_user),
):
    query = select(Contato)
    count_query = select(func.count()).select_from(Contato)

    if empresa_id:
        query = query.where(Contato.empresa_id == empresa_id)
        count_query = count_query.where(Contato.empresa_id == empresa_id)

    if search:
        query = query.where(Contato.nome.ilike(f"%{search}%"))
        count_query = count_query.where(Contato.nome.ilike(f"%{search}%"))

    total = (await db.execute(count_query)).scalar()
    result = await db.execute(query.order_by(Contato.created_at.desc()).offset(skip).limit(limit))
    items = result.scalars().all()

    return ContatoList(items=[ContatoResponse.model_validate(c) for c in items], total=total)


@router.post("", response_model=ContatoResponse, status_code=201)
async def create_contato(
    data: ContatoCreate,
    db: AsyncSession = Depends(get_db),
    _user=Depends(get_current_user),
):
    emp_result = await db.execute(select(Empresa).where(Empresa.id == data.empresa_id))
    if not emp_result.scalar_one_or_none():
        raise HTTPException(status_code=404, detail="Empresa não encontrada")

    contato = Contato(**data.model_dump())
    db.add(contato)
    await db.commit()
    await db.refresh(contato)
    return ContatoResponse.model_validate(contato)


@router.get("/{id}", response_model=ContatoResponse)
async def get_contato(
    id: uuid.UUID,
    db: AsyncSession = Depends(get_db),
    _user=Depends(get_current_user),
):
    result = await db.execute(select(Contato).where(Contato.id == id))
    contato = result.scalar_one_or_none()
    if not contato:
        raise HTTPException(status_code=404, detail="Contato não encontrado")
    return ContatoResponse.model_validate(contato)


@router.put("/{id}", response_model=ContatoResponse)
async def update_contato(
    id: uuid.UUID,
    data: ContatoUpdate,
    db: AsyncSession = Depends(get_db),
    _user=Depends(get_current_user),
):
    result = await db.execute(select(Contato).where(Contato.id == id))
    contato = result.scalar_one_or_none()
    if not contato:
        raise HTTPException(status_code=404, detail="Contato não encontrado")

    update_data = data.model_dump(exclude_unset=True)
    for key, value in update_data.items():
        setattr(contato, key, value)

    await db.commit()
    await db.refresh(contato)
    return ContatoResponse.model_validate(contato)


@router.delete("/{id}", status_code=204)
async def delete_contato(
    id: uuid.UUID,
    db: AsyncSession = Depends(get_db),
    _user=Depends(get_current_user),
):
    result = await db.execute(select(Contato).where(Contato.id == id))
    contato = result.scalar_one_or_none()
    if not contato:
        raise HTTPException(status_code=404, detail="Contato não encontrado")
    contato.ativo = False
    await db.commit()
