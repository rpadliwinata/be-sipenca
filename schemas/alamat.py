from typing import Union
from pydantic import BaseModel
from const import PROVINSI, Base


class AlamatDB(Base):
    provinsi: PROVINSI
    kab_kot: str
    kecamatan: str
    kelurahan: str
    rw: str
    rt: str
    nomor: str


class AlamatOut(BaseModel):
    provinsi: PROVINSI
    kab_kot: str
    kecamatan: str
    kelurahan: str
    rw: Union[str, None] = None
    rt: Union[str, None] = None
    nomor: str
