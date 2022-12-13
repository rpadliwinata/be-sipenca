from uuid import UUID
from .const import Base


class PenyakitDB(Base):
    id_penyakit: UUID
    nama_penyakit: str
