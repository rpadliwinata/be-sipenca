from typing import Union
from uuid import UUID
from .const import Base
from pydantic import BaseModel


class PengelolaDB(Base):
    pengungsian: Union[UUID, str, None] = None
    pengelola: UUID
    is_owner: bool


class PengelolaAdd(BaseModel):
    username: str
    is_owner: bool
