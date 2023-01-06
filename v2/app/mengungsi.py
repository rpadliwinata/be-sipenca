from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.encoders import jsonable_encoder
from pydantic import BaseModel

from db import db_pengungsian, db_profil
from deps import get_current_user
from v2.schemas.pengungsian import PengungsianIn
from v2.schemas.response import ResponseFormat
from v1.schemas.user import UserOut


class Key(BaseModel):
    key: str


router = APIRouter(
    prefix="/mengungsi",
    tags=["mengungsi"],
    dependencies=[Depends(get_current_user)],
)


@router.post("/", response_model=ResponseFormat)
async def mengungsi(key: Key, user: UserOut = Depends(get_current_user)):
    alamat = ""
    res = db_pengungsian.get(key.key)
    if not res:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Pengungsian tidak ditenukan"
        )
    
    try:
        profil = db_profil.fetch({'id_user': user.uuid_})
        if not profil:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Profil tidak ditemukan"
            )

        profil = profil.items[0]
        alamat = profil['alamat_user']
    except:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Alamat belum diupdate"
        )
    
    try:
        pengungsi = res['pengungsi']
    except:
        pengungsi = []

    try:
        data = {
            "alamat": alamat,
            "key": user.key,
            "nama": profil['nama_lengkap']
        }
    except:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Nama lengkap belum diupdate"
        )
    pengungsi.append(data)
    db_pengungsian.update({'pengungsi': pengungsi}, key.key)
    res['pengungsi'] = pengungsi
    
    response = {
        'status': 200,
        'success': True,
        'message': "Berhasil join",
        'data': res
    }

    return response

