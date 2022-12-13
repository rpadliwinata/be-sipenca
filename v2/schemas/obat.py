from uuid import UUID
from const import SATUAN, Base


class ObatDB(Base):
    penyakit: UUID
    nama_obat: str
    satuan: SATUAN
    jumlah: int
