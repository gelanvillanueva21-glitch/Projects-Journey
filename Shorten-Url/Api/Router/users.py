from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.exc import IntegrityError
from typing import Annotated
from database import get_database
from schemas import CreateUser, UserResponse
from crud import get_user_email, create_user
from Router.authentication import get_current_user
from models import User


router = APIRouter(prefix = "/users", tags = ["users"])


@router.post(
    "/register",
    status_code = status.HTTP_201_CREATED,
    response_model = UserResponse)
async def register(
    database : Annotated[AsyncSession, Depends(get_database)],
    user : CreateUser):
        try:
            
            result = await get_user_email(database, user.email)
            if result:
                raise HTTPException(
                    status_code = status.HTTP_400_BAD_REQUEST,
                    detail = "Account already exist"
                )
            data = await create_user(database, user)
            return data
        except IntegrityError:
            raise HTTPException(
                status_code = status.HTTP_400_BAD_REQUEST,
                detail = "Account already exist"
            )


@router.get("/me", response_model = UserResponse)
async def get_user(current_user : Annotated[User, Depends(get_current_user)]):
    return current_user



