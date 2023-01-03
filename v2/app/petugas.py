from fastapi import APIRouter
from v2.schemas.petugas import PetugasOut, PetugasIn
from v2.schemas.response import ResponseFormat
from db import db_user


router = APIRouter(
    prefix="/petugas",
    tags=["petugas"],
)

