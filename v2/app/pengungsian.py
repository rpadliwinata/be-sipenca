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


@router.delete("/", response_model=ResponseFormat)
async def delete_data(key: str):
    res = db_pengungsian.fetch({'key': key})

    db_pengungsian.delete(res.items[0]["key"])
    return {
        'message': "Berhasil hapus data pengungsian!",
        'status': 200,
        'success': True,
        'data': {'list_pengungsian': res.items[0]}
    }


@router.get('/', response_model=ResponseFormat)
async def getAllPengungsian():
    res = db_pengungsian.fetch()
    pengungsian = res.items
    return {
        'status': 200,
        'success': True,
        'message': 'Berhasil menampilkan data pengungsian',
        'data': {'list_pengungsian': pengungsian}}


@router.patch('/update', response_model=ResponseFormat)
async def update_date(key: str, pengungsian: PengungsianIn):
    res = db_pengungsian.fetch({"key": key})

    db_pengungsian.update(pengungsian.dict(), res.items[0]['key'])

    return {
        "message": "Berhasil update data!",
        'status': 200,
        'success': True,
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
