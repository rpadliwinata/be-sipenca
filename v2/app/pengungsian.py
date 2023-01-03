from fastapi import APIRouter, Depends
from fastapi.encoders import jsonable_encoder

from db import db_pengungsian
from deps import get_current_user
from v2.schemas.pengungsian import PengungsianIn
from v2.schemas.response import ResponseFormat

router = APIRouter(
    prefix="/pengungsian",
    tags=["pengungsian"],
    dependencies=[Depends(get_current_user)],
)


@router.get('/', response_model=ResponseFormat)
async def getAllPengungsian():
    res = db_pengungsian.fetch()
    pengungsian = res.items
    return {
        'status': 200,
        'success': True,
        'message': 'Berhasil menampilkan data pengungsian',
        'data': {'list_pengungsian': pengungsian}}


@router.post('/', response_model=ResponseFormat)
async def tambah_pengungsian(pengungsian: PengungsianIn):
    db_pengungsian.put(jsonable_encoder(pengungsian))

    return {
        "status": 200,
        "success": True,
        "message": "Data pengungsian berhasil ditambahkan!",
        "data": {
            "data_pengungsian": pengungsian
        }
    }
