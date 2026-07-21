from datetime import timedelta
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from typing import Annotated
from sqlalchemy.ext.asyncio import AsyncSession
from jose import jwt, JWTError
from database import get_database
from schemas import Token
from crud import get_user_email
from auth import verify_pass, create_jwt
from config import setting

router = APIRouter(
    prefix = "/Auth",
    tags = ["Auth"]
)
oauth2_schema = OAuth2PasswordBearer(tokenUrl = "/Auth/login")



@router.post("/login", response_model = Token)
async def login(
    form_data : Annotated[OAuth2PasswordRequestForm, Depends()],
    database : Annotated[AsyncSession, Depends(get_database)]):
        user = await get_user_email(database, form_data.username)
        if not user or not verify_pass(form_data.password, user.hashed_password):
            raise HTTPException(
                status_code = status.HTTP_401_UNAUTHORIZED,
                detail = "Incorrect email or password",
                headers = {"WWW_Authenticate" : "Bearer"}
            )
        access_token = create_jwt(
            data = {"sub" : user.email},
            expires_delta = timedelta(minutes=30)
        )
        
        return {
            "access_token" : access_token,
            "token_type" : "bearer"
        }


async def get_user(
    token : Annotated[str, Depends(oauth2_schema)],
    database : Annotated[AsyncSession, Depends(get_database)]):
        credentials_exception = HTTPException(
            status_code = status.HTTP_401_UNAUTHORIZED,
            detail = "Could not validate credentials",
            headers = {"WWW-Authenticate" : "Bearer"}
        )
        
        try:
            
            payload = jwt.decode(
                token, setting.secret_key,
                algorithm = [setting.algorithm])
            email : str | None = payload.get("sub")
            
            if email is None:
                raise credentials_exception
        except JWTError:
            raise credentials_exception
        user = await get_user_email(database, email)
        if not user:
            raise credentials_exception
        return user


