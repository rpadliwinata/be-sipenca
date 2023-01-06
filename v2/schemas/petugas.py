from typing import List
from pydantic import BaseModel, SecretStr
from .const import Base
from v2.schemas.pengungsian import PengungsianOut
from v2.schemas.user import UserOut
from v2.schemas.response import ResponseFormat, CustomResponseFormat


class PetugasIn(BaseModel):
    pengungsian: str
    username: str
    is_owner: bool


class PetugasDB(Base):
    pengungsian: PengungsianOut
    user: UserOut
    is_owner: bool


class PetugasOut(BaseModel):
    pengungsian: str
    username: str
    is_owner: bool
    is_active: bool


class PetugasResponse(CustomResponseFormat):
    data: List[PetugasOut]
    
