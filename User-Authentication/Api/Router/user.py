from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.exc import IntegrityError
from typing import Annotated
from database import get_database
from schemas import UserCreate, UserResponse
from crud import get_user_email, create_user
from Router.authentication import get_user
from models import User


router = APIRouter(
    prefix = "/Users",
    tags = ["Users"]
)


@router.post("/register",response_model = UserResponse, status_code = status.HTTP_201_CREATED)
async def register(
    user : UserCreate,
    database : Annotated[AsyncSession, Depends(get_database)]):
        try:
            email_exist = await get_user_email(database, user.email)
            if email_exist:
                raise HTTPException(
                    status_code = status.HTTP_400_BAD_REQUEST,
                    detail = "Email already Registered"
                )
            result = await create_user(database, user)
            return result
        except IntegrityError:
            print(email_exist)
            await database.rollback()
            raise HTTPException(
                status_code = status.HTTP_400_BAD_REQUEST,
                detail = "Email already Registered"
            )


@router.get("/", response_model = UserResponse)
async def read_user(
    current_user : Annotated[User, Depends(get_user)]):
        return current_user



