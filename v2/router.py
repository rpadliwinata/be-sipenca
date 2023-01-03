from fastapi import APIRouter

from v2.app.pengungsian import router as router_pengungsian
from v2.app.akun import router as router_akun
from v2.app.petugas import router as router_petugas


router = APIRouter(
    prefix="/v2"
)

router.include_router(router_pengungsian)
router.include_router(router_akun)
router.include_router(router_petugas)


