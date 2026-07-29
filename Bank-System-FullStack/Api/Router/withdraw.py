from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.ext.asyncio import AsyncSession
from pydantic import Field
from typing import Annotated
from crud import withdraw, get_withdraws, get_balance, delete_deposits_data
from models import Withdraw, User
from hmac_auth import verify_hmac
from Router.authentication import get_current_user, DependencyDatabase



router = APIRouter(prefix = "/withdraw", tags = ["withdraw"])



@router.post("/")
async def withdraw_money(
    database : DependencyDatabase,
    amount : Annotated[int, Query(ge=1000, le=10000)],
    current_user : Annotated[User, Depends(get_current_user)]):
        data = await withdraw(database, current_user.id, amount)
        if not data:
            raise HTTPException(
                status_code = status.HTTP_403_FORBIDDEN,
                detail = "Error occured, can not withdraw"
            )
        balance = await get_balance(database, current_user.id)
        return {
            "status" : "success",
            "withdraw_amount" : data.withdraw_amount,
            "balance" : balance
        }




@router.get("/history")
async def get_history_withdraw(
    database : DependencyDatabase,
    current_user : Annotated[User, Depends(get_current_user)]):
        data = await get_withdraws(database, current_user.id)
        return {
            "status" : "success",
            "data" : data
        }




@router.delete("/history/delete")
async def delete_withdraw_history(
    database : DependencyDatabase,
    current_user : Annotated[User, Depends(get_current_user)]):
        result = await delete_deposits_data(database, current_user.id)
        if not result:
            raise HTTPException(
                status_code = status.HTTP_400_BAD_REQUEST,
                detail = "Withdraw history empty"
            )




