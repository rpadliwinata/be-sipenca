from typing import Union, Any
from datetime import datetime
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer

from v1.schemas.token import TokenPayLoad
from settings import ALGORITHM, JWT_SECRET_KEY
from jose import jwt
from pydantic import ValidationError
from v1.schemas.user import UserOut

from db import db_user

from db import db_user


reusable_oauth = OAuth2PasswordBearer(
    tokenUrl="/v1/akun/login",
    scheme_name="JWT"
)


async def get_current_user(token: str = Depends(reusable_oauth)) -> UserOut:
    try:
        payload = jwt.decode(
            token,
            JWT_SECRET_KEY,
            algorithms=[ALGORITHM]
        )
        token_data = TokenPayLoad(**payload)

        if datetime.fromtimestamp(token_data.exp) < datetime.now():
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Token expired",
                headers={"WWW-Authenticate": "Bearer"}
            )
    except ValidationError:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Couldn't validate credential",
            headers={"WWW-Authenticate": "Bearer"}
        )
        
    # fetch_user = [user for user in static_db if user['user_id'] == token_data.sub]
    fetch_user = db_user.fetch({'uuid_': str(token_data.sub)})
    try:
        user: Union[dict[str, Any], None] = fetch_user.items[0]
    except IndexError:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )
    
    return UserOut(**user)
