from fastapi import APIRouter, Depends, HTTPException, status
from deps import get_current_user
from v1.schemas.profil import ProfilIn
from v1.schemas.user import UserOut
from db import db_profil

router = APIRouter(
    prefix="/profil",
    tags=["profil"],
    dependencies=[Depends(get_current_user)]
)

@router.post("/", response_model=ProfilIn)
async def create_profil(data: ProfilIn, user: UserOut = Depends(get_current_user)):
    req_profil = db_profil.fetch({'id_user': user.uuid_})
    if len(req_profil.items) == 0:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Profile not found"
        )
    
    updates = data.dict()
    updates['tanggal_lahir'] = updates['tanggal_lahir'].strftime("%d/%m/%Y")
    db_profil.update(updates, req_profil.items[0]['key'])
    return updates


@router.get("/", response_model=ProfilIn)
async def get_profil(user: UserOut = Depends(get_current_user)):
    req_profil = db_profil.fetch({'id_user': user.uuid_})
    if len(req_profil.items) == 0:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Profile not found"
        )
    
    return req_profil.items[0]


