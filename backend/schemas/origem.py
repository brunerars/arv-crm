import uuid

from pydantic import BaseModel


class OrigemResponse(BaseModel):
    id: uuid.UUID
    tipo: str
    sub_tipo: str | None
    canal: str | None
    descricao: str | None

    model_config = {"from_attributes": True}
