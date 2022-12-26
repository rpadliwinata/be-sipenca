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


router = APIRouter(
    prefix="/pengungsian",
    tags=["pengungsian"],
    dependencies=[Depends(get_current_user)],
)


@router.get('/')
async def contoh():
    return {'message': 'berhasil'}


