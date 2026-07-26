from datetime import timedelta
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from typing import Annotated
from sqlalchemy.ext.asyncio import AsyncSession
from jose import jwt, JWTError
from database import get_database
from schemas import Token
from crud import get_user_email
from auth import verify_password, create_jwt
from Config.config import settings



# This the variable will use to the auth
# the magic happend in oauth variable
router = APIRouter(prefix = "/auth", tags = ["auth"])
oauth_schema = OAuth2PasswordBearer(tokenUrl = "/auth/login")
DependencyDatabase = Annotated[AsyncSession, Depends(get_database)]



@router.post("/login", response_model = Token)
async def login(
    user_data : Annotated[OAuth2PasswordRequestForm, Depends()],
    database : DependencyDatabase):
        user = await get_user_email(database, user_data.username)
        if not user and not verify_password(user_data.password, user.hashed_password):
            raise HTTPException(
                status_code = status.HTTP_401_UNAUTHORIZED,
                detail = "Incorrect email or password"
            )
            access_token = create_jwt(
                data = {"sub" : user.email},
                expires_delta = timedelta(hours=12)
            )
            return {
                "access_token" : access_token,
                "token_type" : "bearer"
            }




async def get_current_user(
    token : Annotated[str, Depends(oauth_schema)],
    database : DependencyDatabase):
        CredentialException = HTTPException(
            status_code = status.HTTP_401_UNAUTHORIZED,
            detail = "Could not validate credentials",
            headers = {"WWW-Authenticate" : "Bearer"}
        )
        
        try:
            payload = jwt.decode(
                token, settings.secret_key,
                algorithms = [settings.algorithm]
            )
            email : str | None = payload.get("sub")
            if not email:
                raise CredentialException
            
        except JWTError:
            raise CredentialException
        data = await get_user_email(database, email)
        if not data:
            raise CredentialException
        return data









