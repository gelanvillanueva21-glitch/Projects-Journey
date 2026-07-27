from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.ext.asyncio import AsyncSession
from pydantic import Field
from typing import Annotated
from crud import withdraw, get_withdraws
from models import Withdraw, User
from hmac_auth import verify_hmac
from Router.authentication import get_current_user, DependencyDatabase



router = APIRouter(prefix = "/withdraw", tags = ["withdraw"])



@router.post("/")
async def withdraw(
    database : DependencyDatabase,
    amount : Annotated[int, Query(ge=1000, le=10000)],
    current_user : Annotated[User, Depends(get_current_user)]):
        data = await withdraw(database, current_user.id, amount)
        if not data:
            raise HTTPException(
                status_code = status.HTTP_403_FORBIDDEN,
                detail = "Error occured, can not withdraw"
            )
        return {
            "status" : "success",
            "withdraw_amount" : data.withdraw_amount,
            "withdraw_date" : data.date
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




