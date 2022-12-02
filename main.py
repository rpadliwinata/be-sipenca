from v1.router import router as v1
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import RedirectResponse
from utils import *
from db import *
from drive import *
from v1.app.akun import router as router_akun
from v1.app.profil import router as router_profil
from v1.app.pengungsian import router as router_pengungsian
from v1.app.admin import router as router_admin


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

@app.get("/", include_in_schema=False)
async def redirect_docs():
    return RedirectResponse("https://0f9vta.deta.dev/docs")

@app.get("/clear", include_in_schema=False)
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


app.include_router(v1)

# app.include_router(
#     router_akun,
#     prefix="/api",
#     tags=["akun"],
# )

# app.include_router(
#     router_pengungsian,
#     prefix="/api",
#     tags=["pengungsian"],
# )

# app.include_router(
#     router_profil,
#     prefix="/api",
#     tags=["profil"]
# )

# app.include_router(
#     router_admin,
#     prefix="/api",
#     tags=["admin"]
# )
