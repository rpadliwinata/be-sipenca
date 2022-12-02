from typing import List
from fastapi import status, HTTPException, Depends, APIRouter
from fastapi.security import OAuth2PasswordRequestForm
from pydantic import ValidationError
from v1.schemas.user import UserAuth, UserOut, UserDB
from v1.schemas.profil import ProfilDB
from v1.schemas.token import TokenSchema
from uuid import uuid4
from utils import *
from db import db_user, db_profil

router = APIRouter(
    prefix="/akun",
    tags=["akun"],
)

@router.post("/signup", summary="Create new user", response_model=UserOut)
async def create_user(data: UserAuth):
    res = db_user.fetch([{'username': data.username}, {'email': data.email}])
    if len(res.items) != 0:
        if res.items[0]['username'] == data.username:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Username already used"
            )
        elif res.items[0]['email'] == data.email:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Email already used"
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
        'is_active': False if data.role == "pengelola" else True
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



@router.post("/login", summary="Create access and refresh token", response_model=TokenSchema)
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


# @router.get("/me", summary="Get logged in user detail", response_model=UserOut)
# async def get_me(user: UserOut = Depends(get_current_user)):
#     return user


