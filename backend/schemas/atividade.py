import uuid
from datetime import datetime

from pydantic import BaseModel


class AtividadeCreate(BaseModel):
    lead_id: uuid.UUID
    tipo: str
    descricao: str | None = None
    data_prevista: datetime | None = None
    responsavel_id: uuid.UUID | None = None


class AtividadeResponse(BaseModel):
    id: uuid.UUID
    lead_id: uuid.UUID
    responsavel_id: uuid.UUID | None
    tipo: str
    descricao: str | None
    data_prevista: datetime | None
    data_conclusao: datetime | None
    concluida: bool
    created_at: datetime

    model_config = {"from_attributes": True}


class AtividadeList(BaseModel):
    items: list[AtividadeResponse]
    total: int
