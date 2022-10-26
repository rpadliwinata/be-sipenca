from uuid import UUID
from typing import Union
from datetime import date
from .const import Base


class ProfilDB(Base):
    id_user: Union[UUID, str]
    alamat_user: Union[UUID, None] = None
    penyakit: Union[UUID, None] = None
    nama_lengkap: Union[str, None] = None
    kota_lahir: Union[str, None] = None
    tanggal_lahir: Union[date, None] = None
