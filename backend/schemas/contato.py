import uuid
from datetime import datetime

from pydantic import BaseModel, field_validator

NIVEIS_INFLUENCIA = ("decisor", "influenciador", "usuario", "tecnico", "sem_info")


class ContatoCreate(BaseModel):
    empresa_id: uuid.UUID
    nome: str
    cargo: str | None = None
    departamento: str | None = None
    nivel_influencia: str = "sem_info"
    papel_decisao: str | None = None
    email: str | None = None
    telefone_whatsapp: str | None = None
    linkedin: str | None = None
    observacoes: str | None = None

    @field_validator("nivel_influencia")
    @classmethod
    def validate_nivel(cls, v):
        if v not in NIVEIS_INFLUENCIA:
            raise ValueError(f"Nível deve ser: {', '.join(NIVEIS_INFLUENCIA)}")
        return v


class ContatoUpdate(BaseModel):
    nome: str | None = None
    cargo: str | None = None
    departamento: str | None = None
    nivel_influencia: str | None = None
    papel_decisao: str | None = None
    email: str | None = None
    telefone_whatsapp: str | None = None
    linkedin: str | None = None
    ativo: bool | None = None
    observacoes: str | None = None

    @field_validator("nivel_influencia")
    @classmethod
    def validate_nivel(cls, v):
        if v is None:
            return v
        if v not in NIVEIS_INFLUENCIA:
            raise ValueError(f"Nível deve ser: {', '.join(NIVEIS_INFLUENCIA)}")
        return v


class ContatoResponse(BaseModel):
    id: uuid.UUID
    empresa_id: uuid.UUID
    nome: str
    cargo: str | None
    departamento: str | None
    nivel_influencia: str
    papel_decisao: str | None
    email: str | None
    telefone_whatsapp: str | None
    linkedin: str | None
    ativo: bool
    data_cadastro: datetime
    observacoes: str | None
    created_at: datetime
    updated_at: datetime

    model_config = {"from_attributes": True}


class ContatoList(BaseModel):
    items: list[ContatoResponse]
    total: int
