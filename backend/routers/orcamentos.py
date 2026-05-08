"""SPEC §1.3 — endpoints de Orçamento.

Listagem e create são nested em /oportunidades/{opp_id}/orcamentos para refletir
o relacionamento 1:N. Get/update/delete/duplicar usam o id próprio do orçamento."""
import uuid

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from auth_utils import get_current_user
from database import get_db
from schemas.orcamento import OrcamentoCreate, OrcamentoUpdate, OrcamentoResponse
from services.orcamento_service import OrcamentoService

router = APIRouter(tags=["orcamentos"])


@router.get(
    "/oportunidades/{oportunidade_id}/orcamentos",
    response_model=list[OrcamentoResponse],
)
async def list_orcamentos(
    oportunidade_id: uuid.UUID,
    db: AsyncSession = Depends(get_db),
    _user=Depends(get_current_user),
):
    service = OrcamentoService(db)
    items = await service.list_by_oportunidade(oportunidade_id)
    return [OrcamentoResponse.model_validate(o) for o in items]


@router.post(
    "/oportunidades/{oportunidade_id}/orcamentos",
    response_model=OrcamentoResponse,
    status_code=status.HTTP_201_CREATED,
)
async def create_orcamento(
    oportunidade_id: uuid.UUID,
    data: OrcamentoCreate,
    db: AsyncSession = Depends(get_db),
    current_user=Depends(get_current_user),
):
    service = OrcamentoService(db)
    try:
        orc = await service.create(oportunidade_id, data.model_dump(), current_user.id)
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
    return OrcamentoResponse.model_validate(orc)


@router.get("/orcamentos/{id}", response_model=OrcamentoResponse)
async def get_orcamento(
    id: uuid.UUID,
    db: AsyncSession = Depends(get_db),
    _user=Depends(get_current_user),
):
    service = OrcamentoService(db)
    orc = await service.get(id)
    if not orc:
        raise HTTPException(status_code=404, detail="Orcamento nao encontrado")
    return OrcamentoResponse.model_validate(orc)


@router.put("/orcamentos/{id}", response_model=OrcamentoResponse)
async def update_orcamento(
    id: uuid.UUID,
    data: OrcamentoUpdate,
    db: AsyncSession = Depends(get_db),
    _user=Depends(get_current_user),
):
    service = OrcamentoService(db)
    try:
        orc = await service.update(id, data.model_dump(exclude_unset=True))
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
    return OrcamentoResponse.model_validate(orc)


@router.delete("/orcamentos/{id}", status_code=204)
async def delete_orcamento(
    id: uuid.UUID,
    db: AsyncSession = Depends(get_db),
    _user=Depends(get_current_user),
):
    service = OrcamentoService(db)
    try:
        await service.delete(id)
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))


@router.post(
    "/orcamentos/{id}/duplicar",
    response_model=OrcamentoResponse,
    status_code=status.HTTP_201_CREATED,
)
async def duplicar_orcamento(
    id: uuid.UUID,
    db: AsyncSession = Depends(get_db),
    current_user=Depends(get_current_user),
):
    """Cria nova versão a partir de orçamento existente, na mesma oportunidade.
    Reseta flags de envio/aprovação para que a nova versão comece limpa."""
    service = OrcamentoService(db)
    try:
        nova = await service.duplicar(id, current_user.id)
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
    return OrcamentoResponse.model_validate(nova)
