from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from typing import Annotated
from database import get_database
from schemas import UserCreate, UserResponse
from crud import get_user_email, create_user


router = APIRouter(
    prefix = "/Users",
    tags = ["Users"]
)


@router.post("/register", status_code = status.HTTP_201_CREATED)
async def register(
    user : UserCreate,
    database : Annotated[AsyncSession, Depends(get_database)]):
        email_exist = await get_user_email(database, user.email)
        try:
            if email_exist:
                raise HTTPException(
                    status_code = status.HTTP_400_BAD_REQUEST,
                    detail = "Emainl already Registered"
                )
            return await create_user(database, user)
        except Exception as e:
            database.rollback()
            raise HTTPException(
                status_code = status.HTTP_400_BAD_REQUEST,
                detail = "Email already Registered"
            )


@router.get("/", response_model = UserResponse)
async def read_user():
    pass



