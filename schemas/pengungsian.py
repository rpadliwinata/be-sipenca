from typing import Union
from uuid import UUID
from pydantic import BaseModel
from .const import Base


class PengungsianDB(Base):
    alamat: Union[UUID, str, None] = None
    nama_tempat: str
    kapasitas_tempat: int
    gambar_tempat: Union[str, None] = None


class PengungsianIn(BaseModel):
    alamat: Union[UUID, str, None] = None
    nama_tempat: str
    kapasitas_tempat: int


class PengungsianOut(BaseModel):
    nama_tempat: str
    kapasitas_tempat: int
    gambar_tempat: Union[str, None] = None


class PengungsianGet(BaseModel):
    uuid_: str
    nama_tempat: str
    owner: str
    alamat: str
