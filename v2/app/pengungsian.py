
from fastapi import APIRouter, Depends
from deps import get_current_user
from v2.schemas.response import ResponseFormat
from fastapi import APIRouter, Depends
from deps import get_current_user
from db import db_pengungsian

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
        'status' : 200,
        'success' :True,
        'data': {'list_pengungsian':res.items[0]}
    }



