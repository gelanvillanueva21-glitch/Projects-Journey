from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.exc import IntegrityError
from pydantic import EmailStr
from typing import Annotated
from schemas import UserResponse, CreateUser
from crud import create_user_account, get_user_email, change_user_password, get_balance
from Router.authentication import get_current_user, DependencyDatabase
from models import User
from auth import hash_password



router = APIRouter(prefix = "/user", tags = ["user"])



@router.post("/create", response_model = UserResponse, status_code = status.HTTP_201_CREATED)
async def create_user(
    database : DependencyDatabase,
    user_data : CreateUser):
        try:
            email_exist = await get_user_email(database, user_data.email)
            print("Computer Science")
            if email_exist:
                print(email_exist)
                raise HTTPException(
                    status_code = status.HTTP_400_BAD_REQUEST,
                    detail = "Email already registered"
                )
            data = await create_user_account(database, user_data)
            print("Sayonara")
            return data
        except IntegrityError:
            await database.rollback()
            raise HTTPException(
                status_code = status.HTTP_400_BAD_REQUEST,
                detail = "An error occured during creating account"
            )




@router.put("/change_password")
async def change_password(
    database : DependencyDatabase,
    current_password : Annotated[str, Query(min_length=8, max_length=50)],
    new_password : Annotated[str, Query(min_length=8, max_length=50)],
    current_user : Annotated[User, Depends(get_current_user)]):
        try:
            is_changed = await change_user_password(
                database,
                current_password,
                hash_password(new_password),
                current_user)
            if not is_changed:
                raise HTTPException(
                    status_code = status.HTTP_400_BAD_REQUEST,
                    detail = "Current password incorrect"
                )
            return {"status" : "success"}
        except IntegrityError:
            await database.rollback()
            raise HTTPException(
                status_code = status.HTTP_400_BAD_REQUEST,
                detail = "An error occured during changing password"
            )




@router.get("/me", response_model = UserResponse)
async def get_info(current_user_info : Annotated[
    User, Depends(get_current_user)]):
        return current_user_info




@router.get("/balance")
async def get_user_balance(
    database : DependencyDatabase,
    current_user : Annotated[User, Depends(get_current_user)]):
        return await get_balance(database, current_user.id)





