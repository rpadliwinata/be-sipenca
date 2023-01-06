from datetime import date
from typing import Union
from uuid import UUID

from pydantic import BaseModel

from v1.schemas.alamat import AlamatOut

from .const import Base


class ProfilDB(Base):
    id_user: Union[UUID, str]
    alamat_user: Union[str, None] = None
    penyakit: Union[UUID, None] = None
    nama_lengkap: Union[str, None] = None
    no_tlp: Union[str, None] = None
    kota_lahir: Union[str, None] = None
    tanggal_lahir: Union[date, None] = None


class ProfilIn(BaseModel):
    alamat_user: Union[str, str, None] = None
    penyakit: Union[UUID, str, None] = None
    nama_lengkap: Union[str, None] = None
    no_tlp: Union[str, None] = None
    kota_lahir: Union[str, None] = None
    tanggal_lahir: Union[date, str, None] = None
