from fastapi import APIRouter, Depends
from deps import get_current_user
from v2.schemas.response import ResponseFormat
from db import db_pengungsian


router = APIRouter(
    prefix="/pengungsian",
    tags=["pengungsian"],
    dependencies=[Depends(get_current_user)],
)

@router.get('/', response_model= ResponseFormat)
async def getAllPengungsian():
    res = db_pengungsian.fetch()
    pengungsian = res.items
    return {
        'status': 200, 
        'success': True,
        'message': 'Berhasil menampilkan data pengungsian',
        'data':{'list_pengungsian':pengungsian}}