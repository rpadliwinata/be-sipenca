from fastapi import APIRouter, Depends
from deps import get_current_user
from v2.schemas.response import ResponseFormat
from db import db_pengungsian


router = APIRouter(
    prefix="/pengungsian",
    tags=["pengungsian"],
    dependencies=[Depends(get_current_user)],
)

