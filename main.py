from typing import List
from fastapi import FastAPI, status, HTTPException, File, UploadFile, Depends
from fastapi.security import OAuth2PasswordRequestForm
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import StreamingResponse, RedirectResponse
from pydantic import ValidationError
from schemas.alamat import AlamatDB
from schemas.user import UserAuth, UserOut, UserDB
from schemas.profil import ProfilDB, ProfilIn
from schemas.pengungsian import *
from schemas.pengelola import *
from schemas.token import TokenSchema
from uuid import uuid4
from deps import get_current_user
from utils import *
from db import *
from drive import *


app = FastAPI(
    title="Sipenca",
    version="0.0.1",
    prefix="/api"
)

origins = [
    "http://localhost",
    "http://localhost:8000",
    "http://localhost:3000",
    "https://sipenca.my.id"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)

@app.get("/")
async def redirect_docs():
    return RedirectResponse("https://0f9vta.deta.dev/docs")


@app.post("/api/signup", summary="Create new user", response_model=UserOut)
async def create_user(data: UserAuth):
    res = db_user.fetch([{'username': data.username}, {'email': data.email}])
    if len(res.items) != 0:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="User alrady exist"
        )
    
    new_user = {
        'uuid_': str(uuid4()),
        'created_at': datetime.now().strftime("%m/%d/%Y, %H:%M:%S"),
        'uuid_': str(uuid4()),
        'created_at': datetime.now().strftime("%m/%d/%Y, %H:%M:%S"),
        'email': data.email,
        'username': data.username,
        'hashed_password': get_hashed_password(data.password),
        'role': data.role,
        'is_active': False
    }
    try:
        validated_new_user = UserDB(**new_user)
        db_user.put(validated_new_user.dict())
    except ValidationError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid input value"
        )
    try:
        validated_new_user = UserDB(**new_user)
        db_user.put(validated_new_user.dict())
    except ValidationError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid input value"
        )
    
    new_profile = {
        'uuid_': str(uuid4()),
        'created_at': datetime.now().strftime("%m/%d/%Y, %H:%M:%S"),
        'created_by': new_user['uuid_'],
        'id_user': new_user['uuid_']
    }
    try:
        validated_new_profile = ProfilDB(**new_profile)
        db_profil.put(new_profile)
    except ValidationError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid input value"
        )
    
    return validated_new_user.dict()



@app.post("/api/login", summary="Create access and refresh token", response_model=TokenSchema)
async def login(form_data: OAuth2PasswordRequestForm = Depends()):
    # req_user = [user for user in static_db if user['username'] == form_data.username][0]
    req_user = db_user.fetch({'username': form_data.username})
    if len(req_user.items) == 0:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Username not found"
        )
    
    req_user = req_user.items[0]
    hashed_pass = req_user['hashed_password']
    if not verify_password(form_data.password, hashed_pass):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Wrong password"
        )
    
    return {
        'access_token': create_access_token(req_user['uuid_']),
        'refresh_token': create_refresh_token(req_user['uuid_'])
    }


# @app.post("/api/profile/", response_model=ProfilIn)
# async def create_profile(data: ProfilIn, user: UserOut = Depends(get_current_user)):


@app.get("/api/me", summary="Get logged in user detail", response_model=UserOut)
async def get_me(user: UserOut = Depends(get_current_user)):
    return user


@app.get("/api/pengungsian")
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
        kota = profil['alamat']['kab_kot']

        req_pengungsian = db_pengungsian.fetch({'alamat.kab_kot': kota})
        if len(req_pengungsian.items) == 0:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Data not found"
            )
        
        return req_pengungsian.items



@app.post("/api/pengungsian/daftar", response_model=PengungsianIn)
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


@app.post("/api/pengungsian/gambar", response_model=PengungsianOut)
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
    
    return pengungsian.dict()


@app.post("/api/pengungsian/pengelola", response_model=PengelolaDB)
async def tambah_pengelola(username: str, user: UserOut = Depends(get_current_user)):
    req_pengelola = db_user.fetch({'username': username})
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


@app.get("/api/pengungsian/gambar")
async def get_image(user: UserOut = Depends(get_current_user)):
    req_pengungsian = db_pengungsian.fetch({'created_by': str(user.uuid_)})
    if len(req_pengungsian.items) == 0:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="No records found"
        )
    req_gambar = drive_pengungsian.get(req_pengungsian.items[0]['gambar_tempat'])

    return StreamingResponse(req_gambar.iter_chunks(4096), media_type="image/jpg")

# {
#   "alamat": {
#     "provinsi": "Jawa Barat",
#     "kab_kot": "Bandung",
#     "kecamatan": "Cinambo",
#     "kelurahan": "Cisaranten Wetan",
#     "rw": "01",
#     "rt": "01",
#     "nomor": "71"
#   },
#   "nama_tempat": "Rumah Saya",
#   "kapasitas_tempat": 30
# }

@app.get("/clear")
async def clear_db():
    req_pengungsian = db_pengungsian.fetch().items
    req_pengelola = db_pengelola.fetch().items
    req_alamat = db_alamat.fetch().items
    
    for item in req_pengungsian:
        db_pengungsian.delete(item['key'])
    
    for item in req_pengelola:
        db_pengelola.delete(item['key'])
    
    for item in req_alamat:
        db_alamat.delete(item['key'])
    
    return {'message': 'success'}
