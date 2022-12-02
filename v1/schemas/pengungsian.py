from typing import Union
from uuid import UUID
from pydantic import BaseModel
from .const import Base
from v1.schemas.alamat import AlamatOut


class PengungsianDB(Base):
    alamat: Union[AlamatOut, None] = None
    nama_tempat: str
    kapasitas_tempat: int
    gambar_tempat: Union[str, None] = None
    is_active: bool = False


class PengungsianIn(BaseModel):
    alamat: AlamatOut
    nama_tempat: str
    kapasitas_tempat: int


class PengungsianOut(BaseModel):
    nama_tempat: str
    kapasitas_tempat: int
    gambar_tempat: Union[str, None] = None


class PengungsianGet(BaseModel):
    uuid_: str
    nama_tempat: str
    kapasitas_tempat: int
    gambar_tempat: Union[str, None] = None
    is_active: bool = False
