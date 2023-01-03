from deta import Deta
from settings import PROJECT_KEY

deta = Deta(PROJECT_KEY)

db_alamat = deta.Base("db_alamat")
db_user = deta.Base("db_user")
db_kebutuhan = deta.Base("db_kebutuhan")
db_keluarga = deta.Base("db_keluarga")
db_obat = deta.Base("db_obat")
db_pengelola = deta.Base("db_pengelola")
db_pengungsian = deta.Base("db_pengungsian")
db_penyakit = deta.Base("db_penyakit")
db_profil = deta.Base("db_profil")
db_role = deta.Base("db_role")
db_petugas = deta.Base("db_petugas")



