from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.encoders import jsonable_encoder
from pydantic import BaseModel

from db import db_pengungsian, db_profil, db_user, db_m2m
from deps import get_current_user
from v2.schemas.petugas import PetugasResponse
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
    db_user.update({'is_join': True}, user.key)
    db_pengungsian.update({'pengungsi': pengungsi}, key.key)
    db_m2m.put({'pengungsian': key.key, 'user': user.key})
    res['pengungsi'] = pengungsi
    
    response = {
        'status': 200,
        'success': True,
        'message': "Berhasil join",
        'data': res
    }

    return response


@router.delete("/", response_model=ResponseFormat)
async def keluar_dari_pengungsian(user: UserOut = Depends(get_current_user)):
    if not user.is_join:
        raise HTTPException(
            status_code=400,
            detail="Belum join ke pengungsian"
        )
    key = db_m2m.fetch({'user': user.key}).items[0]
    key = key['pengungsian']
    res = db_pengungsian.get(key)
    
    pengungsi = res['pengungsi']
    pengungsi = [x for x in pengungsi if x['key'] != user.key]
    res['pengungsi'] = pengungsi
    
    db_pengungsian.update({'pengungsi': pengungsi}, key)
    db_user.update({'is_join': False}, user.key)
    
    return {
        'status': 200,
        'success': True,
        'message': "Berhasil meninggalkan pengungsian",
        'data': res
    }


