from uuid import UUID
from const import SATUAN, Base


class KebutuhanDB(Base):
    keluarga: UUID
    nama_barang: str
    satuan: SATUAN
    jumlah: int
    is_primary: bool
