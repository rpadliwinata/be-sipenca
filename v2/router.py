from fastapi import APIRouter

from v2.app.pengungsian import router as router_pengungsian


router = APIRouter(
    prefix="/v2"
)

router.include_router(router_pengungsian)
