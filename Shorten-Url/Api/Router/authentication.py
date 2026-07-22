from datetime import timedelta
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from typing import Annotated
from sqlalchemy.ext.asyncio import AsyncSession
from jose import jwt, JWTError
from database import get_database
from schemas import TokenResponse
from crud import get_user_email
from auth import verify_password, create_jwt
from config import settings



router = APIRouter(prefix = "/auth", tags = ["auth"])
oath2_schemas = OAuth2PasswordBearer(tokenUrl = "/auth/login")



@router.post(
    "/login",
    status_code = status.HTTP_200_OK,
    response_model = TokenResponse)
async def login(
    user_data : Annotated[OAuth2PasswordRequestForm, Depends()],
    database : Annotated[AsyncSession, Depends(get_database)]):
        user = await get_user_email(database, user_data.username)
        if not user or not verify_password(user_data.password, user.hashed_password):
            raise HTTPException(
                status_code = status.HTTP_401_UNAUTHORIZED,
                detail = "Incorrect Email or Password",
                headers = {"WWW-Authenticate" : "Bearer"}
            )
        access_token = create_jwt(
            data = {"sub" : user.email},
            expires_delta = timedelta(minutes=30)
        )
        return {
            "access_token" : access_token,
            "token_type" : "bearer"
        }



async def get_current_user(
    token : Annotated[str, Depends(oath2_schemas)],
    database : Annotated[AsyncSession, Depends(get_database)]):
        credential_exception = HTTPException(
            status_code = status.HTTP_401_UNAUTHORIZED,
            detail = "Could not validate credentials",
            headers = {"WWW-Authenticate" : "Bearer"}
        )
        try:
            
            payload = jwt.decode(
                token,
                settings.secret_key,
                algorithm = [settings.algorithm]
            )
            email : str | None = payload.get("sub")
            if not email:
                raise credential_exception
        except JWTError:
            raise credential_exception
        user = await get_user_email(database, email)
        
        if not user:
            raise credential_exception
        return user



