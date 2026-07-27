from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.exc import IntegrityError
from typing import Annotated
from schemas import UserResponse, CreateUser
from crud import create_user_account, get_user_email
from Router.authentication import get_current_user, DependencyDatabase
from models import User



router = APIRouter(prefix = "/user", tags = ["user"])



@router.post("/create", response_model = UserResponse, status_code = status.HTTP_201_CREATED)
async def create_user(
    database : DependencyDatabase,
    user_data : CreateUser):
        try:
            email_exist = await get_user_email(database, user_data.email)
            if email_exist:
                print(email_exist)
                raise HTTPException(
                    status_code = status.HTTP_400_BAD_REQUEST,
                    detail = "Email already registered"
                )
            data = await create_user_account(database, user_data)
            return data
        except IntegrityError:
            await database.rollback()
            raise HTTPException(
                status_code = status.HTTP_400_BAD_REQUEST,
                detail = "Email already registered"
            )




@router.get("/me", response_model = UserResponse)
async def get_info(current_user_info : Annotated[
    User, Depends(get_current_user)]):
        return current_user_info





