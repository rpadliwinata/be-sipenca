from typing import List
from fastapi import APIRouter, Depends, HTTPException, status
from deps import get_current_user
from v1.schemas.user import UserOut, PengelolaInput
from db import db_user

router = APIRouter(
    prefix="/admin",
    tags=["admin"],
    dependencies=[Depends(get_current_user)]
)

@router.post("/approve/akun", response_model=UserOut)
async def approve_akun(data: PengelolaInput, user: UserOut = Depends(get_current_user)):
    req_user = db_user.fetch({'uuid_': data.uuid_})
    if len(req_user.items) == 0:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )
    
    user = req_user.items[0]
    user['is_active'] = True
    print(user)
    print(req_user.items[0]['key'])
    db_user.update(user, req_user.items[0]['key'])
    return user


@router.get("/list/pengelola", response_model=List[UserOut])
async def list_pengelola(user: UserOut = Depends(get_current_user)):
    if user.role != "admin":
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Restricted access"
        )
    
    req_user = db_user.fetch({'role': 'pengelola'})
    if len(req_user.items) == 0:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="No data found"
        )
    
    return req_user.items
