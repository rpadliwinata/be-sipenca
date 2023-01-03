from fastapi import APIRouter, Depends
from deps import get_current_user
from v2.schemas.response import ResponseFormat
from db import db_pengungsian


router = APIRouter(
    prefix="/pengungsian",
    tags=["pengungsian"],
)


@router.get('/', response_model=ResponseFormat)
async def nama_fungsi():
    res = db_pengungsian.fetch()
    pengungsian = res.items
    return {
        'message': 'Berhasil',
        'success': True,
        'status': 200,
        'data': {
            'list_pengungsian': pengungsian
        }
    }
