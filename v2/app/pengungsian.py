from datetime import datetime
from typing import List
from uuid import UUID, uuid4

from deta import Deta
from fastapi import APIRouter, Depends, HTTPException, UploadFile, status
from fastapi.encoders import jsonable_encoder
from fastapi.responses import StreamingResponse
from pydantic import BaseModel, ValidationError

from db import db_alamat, db_pengelola, db_pengungsian, db_profil, db_user
from deps import get_current_user
from drive import drive_pengungsian
from v2.schemas.alamat import AlamatDB
from v2.schemas.pengelola import PengelolaAdd, PengelolaDB, PengelolaOut
from v2.schemas.pengungsian import (PengungsianDB, PengungsianGet,
                                    PengungsianIn, PengungsianOut)
from v2.schemas.user import UserOut

router = APIRouter(
    prefix="/pengungsian",
    tags=["pengungsian"],
    # dependencies=[Depends(get_current_user)],
)


class Data(BaseModel):
    username: str
    role: str


deta = Deta("c0xyaz4k_HiLWrZZpCCXESBZZXe6LAsMcSp3dnx1f")
db = deta.Base("db_pengungsian")


@router.get('/')
async def contoh():
    res = db.fetch()
    return {'message': 'berhasil', "data": res.items}


@router.post('/tambah')
async def tambah_pengungsian(params: PengungsianIn):
    db.put(jsonable_encoder(params))

    response = {
        "status": 200,
        "success": True,
        "message": "Data pengungsian berhasil ditambahkan!",
        "data": params
    }

    return response
