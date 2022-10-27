from uuid import UUID
from typing import Union
from datetime import date

from pydantic import BaseModel
from .const import Base
from schemas.alamat import AlamatOut


class ProfilDB(Base):
    id_user: Union[UUID, str]
    alamat_user: Union[AlamatOut, None] = None
    penyakit: Union[UUID, None] = None
    nama_lengkap: Union[str, None] = None
    kota_lahir: Union[str, None] = None
    tanggal_lahir: Union[date, None] = None


class ProfilIn(BaseModel):
    alamat_user: Union[AlamatOut, str, None] = None
    penyakit: Union[UUID, str, None] = None
    nama_lengkap: Union[str, None] = None
    kota_lahir: Union[str, None] = None
    tanggal_lahir: Union[date, str, None] = None
