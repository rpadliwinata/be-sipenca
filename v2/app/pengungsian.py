
from fastapi import APIRouter, Depends
from deps import get_current_user
from deta import Deta
from fastapi import FastAPI
from v2.schemas import pengungsian
from v2.schemas.response import ResponseFormat
from deta import Deta
from fastapi import APIRouter, Depends
from deps import get_current_user

deta = Deta("c0xyaz4k_HiLWrZZpCCXESBZZXe6LAsMcSp3dnx1f")
db = deta.Base("db_pengungsian")
app = FastAPI(title="Sipenca")

router = APIRouter(
    prefix="/pengungsian",
    tags=["pengungsian"],
    dependencies=[Depends(get_current_user)],
)

@router.delete("/", response_model=ResponseFormat)
async def delete_data(key: str):
    res = db.fetch({'key': key})

    db.delete(res.items[0]["key"])
    return {
        'message': "Berhasil hapus data pengungsian!",
        'status' : 200,
        'success' :True,
        'data': {'list_pengungsian':pengungsian}
    }



