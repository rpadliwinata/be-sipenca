from deta import Deta
from fastapi import APIRouter, Depends
from fastapi.encoders import jsonable_encoder
from pydantic import BaseModel

from deps import get_current_user
from v2.schemas.pengungsian import PengungsianIn
from v2.schemas.response import ResponseFormat

router = APIRouter(
    prefix="/pengungsian",
    tags=["pengungsian"],
    dependencies=[Depends(get_current_user)],
)

deta = Deta("c0xyaz4k_HiLWrZZpCCXESBZZXe6LAsMcSp3dnx1f")
db = deta.Base("db_pengungsian")


@router.get('/')
async def contoh():
    res = db.fetch()

    response = {
        "status": 200,
        "success": True,
        "message": "Data pengungsian berhasil ditambahkan!",
        "data": res.items
    }

    return response


@router.post('/', response_model=ResponseFormat)
async def tambah_pengungsian(params: PengungsianIn):
    db.put(jsonable_encoder(params))

    return {
        "status": 200,
        "success": True,
        "message": "Data pengungsian berhasil ditambahkan!",
        "data": params
    }
