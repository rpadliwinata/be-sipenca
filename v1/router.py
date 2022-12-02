from fastapi import APIRouter
from v1.app.admin import router as admin_router
from v1.app.akun import router as akun_router
from v1.app.pengungsian import router as pengungsian_router
from v1.app.profil import router as profil_router

router = APIRouter(
    prefix="/v1"
)

router.include_router(admin_router)
router.include_router(akun_router)
router.include_router(pengungsian_router)
router.include_router(profil_router)
