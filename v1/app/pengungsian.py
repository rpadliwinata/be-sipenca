from uuid import uuid4, UUID
from datetime import datetime
from typing import List
from fastapi import APIRouter, Depends, HTTPException, status, UploadFile
from fastapi.responses import StreamingResponse
from pydantic import ValidationError
from deps import get_current_user
from v1.schemas.alamat import AlamatDB
from v1.schemas.pengelola import PengelolaDB, PengelolaAdd, PengelolaOut
from v1.schemas.pengungsian import PengungsianGet, PengungsianIn, PengungsianDB, PengungsianOut
from v1.schemas.user import UserOut
from db import db_profil, db_pengelola, db_pengungsian, db_alamat, db_user
from drive import drive_pengungsian

router = APIRouter(
    prefix="/pengungsian",
    tags=["pengungsian"],
    dependencies=[Depends(get_current_user)],
)


@router.get("/", response_model=List[PengungsianGet])
async def get_pengungsian(user: UserOut = Depends(get_current_user)):
    if user.role == "pengelola":
        req_pengelola = db_pengelola.fetch({'pengelola': user.uuid_})
        if len(req_pengelola.items) == 0:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Data not found"
            )
        pengungsian = [item['pengungsian'] for item in req_pengelola.items]
        req_pengungsian = [db_pengungsian.fetch({'uuid_': item}).items[0] for item in pengungsian]
        return req_pengungsian
    else:
        req_profil = db_profil.fetch({"id_user": user.uuid_})
        if len(req_profil.items) == 0:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Profile not found"
            )
        profil = req_profil.items[0]
        kota = profil['alamat_user']['kab_kot']

        req_pengungsian = db_pengungsian.fetch({'alamat.kab_kot': kota})
        if len(req_pengungsian.items) == 0:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Data not found"
            )
        
        return req_pengungsian.items



@router.post("/", response_model=PengungsianIn)
async def daftar_pengungsian(data: PengungsianIn, user: UserOut = Depends(get_current_user)):
    if user.role != "pengelola":
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Unauthorized user"
        )

    req_pengungsian = db_pengungsian.fetch({'nama_tempat': data.nama_tempat})
    if len(req_pengungsian.items) != 0:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Data already exist"
        )
    
    new_alamat = {
        'uuid_': str(uuid4()),
        'created_at': datetime.now().strftime("%m/%d/%Y, %H:%M:%S"),
        'created_by': user.uuid_,
        'provinsi': data.alamat.provinsi,
        'kab_kot': data.alamat.kab_kot,
        'kecamatan': data.alamat.kecamatan,
        'kelurahan': data.alamat.kelurahan,
        'rw': data.alamat.rw,
        'rt': data.alamat.rt,
        'nomor': data.alamat.nomor,
    }
    
    new_pengungsian = {
        'uuid_': str(uuid4()),
        'created_at': datetime.now().strftime("%m/%d/%Y, %H:%M:%S"),
        'created_by': user.uuid_,
        'alamat': data.alamat.dict(),
        'nama_tempat': data.nama_tempat,
        'kapasitas_tempat': data.kapasitas_tempat
    }

    new_pengelola = {
        'uuid_': str(uuid4()),
        'created_at': datetime.now().strftime("%m/%d/%Y, %H:%M:%S"),
        'created_by': user.uuid_,
        'pengungsian': new_pengungsian['uuid_'],
        'pengelola': user.uuid_,
        'is_owner': True
    }
    
    try:
        validated_new_alamat = AlamatDB(**new_alamat)
        validated_new_pengelola = PengelolaDB(**new_pengelola)
        validated_new_pengungsian = PengungsianDB(**new_pengungsian)
    except ValidationError:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid data"
        )
    db_alamat.put(new_alamat)
    db_pengelola.put(new_pengelola)
    db_pengungsian.put(new_pengungsian)
    
    return validated_new_pengungsian


@router.post("/gambar", response_model=PengungsianOut)
async def upload_foto_pengungsian(uuid_pengungsian: str, img: UploadFile, user: UserOut = Depends(get_current_user)):
    # req_pengungsian = db_pengungsian.fetch({'created_by': str(user.uuid_)})
    req_pengungsian = db_pengungsian.fetch({'uuid_': uuid_pengungsian})

    if len(req_pengungsian.items) == 0:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Data not exist"
        )
    
    file_content = await img.read()
    filename = f"{req_pengungsian.items[0]['nama_tempat']}_{user.username}.jpg"
    drive_pengungsian.put(filename, file_content)
    
    update = {
        'gambar_tempat': filename
    }
    pengungsian = req_pengungsian.items[0]
    pengungsian['gambar_tempat'] = filename
    db_pengungsian.update(update, pengungsian['key'])
    
    return pengungsian


@router.post("/pengelola", response_model=PengelolaOut)
async def tambah_pengelola(data: PengelolaAdd, user: UserOut = Depends(get_current_user)):
    req_pengelola = db_user.fetch({'username': data.username})
    if len(req_pengelola.items) == 0:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )
    
    req_pengungsian = db_pengungsian.fetch({'created_by': str(user.uuid_)})
    if len(req_pengungsian.items) == 0:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Item not found"
        )
    
    new_pengelola = {
        'uuid_': str(uuid4()),
        'created_at': datetime.now().strftime("%m/%d/%Y, %H:%M:%S"),
        'created_by': UUID(user.uuid_),
        'pengungsian': UUID(req_pengungsian.items[0]['uuid_']),
        'pengelola': UUID(req_pengelola.items[0]['uuid_']),
        'is_owner': False
    }
    
    try:
        validated_new_pengelola = PengelolaDB(**new_pengelola)
        new_pengelola['created_by'] = str(new_pengelola['created_by'])
        new_pengelola['pengungsian'] = str(new_pengelola['pengungsian'])
        new_pengelola['pengelola'] = str(new_pengelola['pengelola'])
        db_pengelola.put(new_pengelola)
    except ValidationError as e:
        print(e)
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid value"
        )
    
    return new_pengelola


@router.get("/gambar")
async def get_image(user: UserOut = Depends(get_current_user)):
    req_pengungsian = db_pengungsian.fetch({'created_by': str(user.uuid_)})
    if len(req_pengungsian.items) == 0:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="No records found"
        )
    req_gambar = drive_pengungsian.get(req_pengungsian.items[0]['gambar_tempat'])

    return StreamingResponse(req_gambar.iter_chunks(4096), media_type="image/jpg")
