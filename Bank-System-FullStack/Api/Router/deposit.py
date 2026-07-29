from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.ext.asyncio import AsyncSession
from typing import Annotated
from pydantic import Field
from crud import deposit, get_deposits, delete_deposits_data
from models import User, Deposit
from Router.authentication import DependencyDatabase, get_current_user



router = APIRouter(prefix = "/deposit", tags = ["deposit"])



@router.post("/")
async def deposit_amount(
    database : DependencyDatabase,
    amount : Annotated[int, Query(ge=100, le=10000)],
    current_user : Annotated[User, Depends(get_current_user)]):
        data = await deposit(database, current_user.id, amount)
        if not data:
            raise HTTPException(
                status_code = status.HTTP_400_BAD_REQUEST,
                detail = "Error occured during deposit"
            )
        return {
            "status" : "success",
            "balance" : data
        }




@router.get("/history")
async def get_deposit_history(
    database : DependencyDatabase,
    current_user : Annotated[User, Depends(get_current_user)]):
        data = await get_deposits(database, current_user.id)
        return {
            "status" : "success",
            "data" : data
        }




@router.delete("/history/delete")
async def delete_deposit_history(
    database : DependencyDatabase,
    current_user : Annotated[User, Depends(get_current_user)]):
        result = await delete_deposits_data(database, current_user.id)
        if not result:
            raise HTTPException(
                status_code = status.HTTP_400_BAD_REQUEST,
                detail = "Deposits history empty"
            )
        return {"status" : "success"}








