from uuid import uuid4, UUID
from datetime import datetime
from typing import List
from fastapi import APIRouter, Depends, HTTPException, status, UploadFile
from fastapi.responses import StreamingResponse
from pydantic import ValidationError
from deps import get_current_user
from v2.schemas.alamat import AlamatDB
from v2.schemas.pengelola import PengelolaDB, PengelolaAdd, PengelolaOut
from v2.schemas.pengungsian import PengungsianGet, PengungsianIn, PengungsianDB, PengungsianOut
from v2.schemas.user import UserOut
from db import db_profil, db_pengelola, db_pengungsian, db_alamat, db_user
from drive import drive_pengungsian
from deta import Deta
from fastapi import FastAPI

deta = Deta("c0xyaz4k_HiLWrZZpCCXESBZZXe6LAsMcSp3dnx1f")
db = deta.Base("db_pengungsian")
app = FastAPI(title="Sipenca")

router = APIRouter(
    prefix="/pengungsian",
    tags=["pengungsian"],
    # dependencies=[Depends(get_current_user)],
)

# @router.get('/')
# async def contoh():
#     return {'message': 'berhasil'}


@router.delete('/')
async def delete_data(key: str):
    res = db.fetch({"key": key})

    db.delete(res.items[0]["key"])
    return {
        "message": "Berhasil hapus data!"
    }
