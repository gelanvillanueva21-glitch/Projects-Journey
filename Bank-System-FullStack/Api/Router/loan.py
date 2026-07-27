from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.ext.asyncio import AsyncSession
from pydantic import Field
from typing import Annotated
from Router.authentication import get_current_user, DependencyDatabase
from schemas import LoanMoney, LoanPay, LoanRespons
from models import LoanHistory, Loan, LoanPayment, User
from crud import get_archived_loan, borrow_money, payment, active_lend, lend_amount, get_available_lenders
from hmac_auth import verify_hmac



router = APIRouter(prefix = "/loan", tags = ["loan"])



@router.post("/", response_model = LoanRespons)
async def borrow(
    database : DependencyDatabase,
    current_user : Annotated[User, Depends(get_current_user)],
    lender_user : int,
    signature : str,
    loan : LoanMoney):
    result = verify_hmac(str(lender_user).encode("utf-8"), signature.encode("utf-8"))
    if result:
        data = await borrow_money(database, loan, current_user.id, lender_user)
        if isinstance(data, str):
            raise HTTPException(
                status_code = status.HTTP_400_BAD_REQUEST,
                detail = data
            )
        return data
    raise HTTPException(
        status_code = status.HTTP_401_UNAUTHORIZED,
        detail = "Unauthorized data trying to access database"
    )



@router.post("/pay", response_model = LoanPay)
async def loan_payment(
    database : DependencyDatabase,
    payment_info : LoanPay,
    lender_user : int,
    signature : str,
    current_user : Annotated[User, Depends(get_current_user)]):
        result = verify_hmac(str(lender_user).encode("utf-8"), signature.encode("utf-8"))
        data = await payment(
            database, 
            payment_info, 
            current_user.id, 
            lender_user)
        if isinstance(data, str) or data is None:
            raise HTTPException(
                status_code = status.HTTP_400_BAD_REQUEST,
                detail = data if data else "Error occured during payment"
            )
        return {"paid_amount" : data.paid_amount}








@router.post("/activate")
async def activate_lender(
    database : DependencyDatabase,
    amount : Annotated[int, Query(ge=1000, le=10000)],
    current_user : Annotated[User, Depends(get_current_user)]):

        result = await active_lend(database, get_current_user.id)
        if not result:
            raise HTTPException(status_code = status.HTTP_400_BAD_REQUEST)
        data = await lend_amount(database, current_user.id, amount)
        if not data:
            raise HTTPException(status_code = status.HTTP_400_BAD_REQUEST)
        return {"status" : "success"}



@router.get("/lenders")
async def get_lenders(database : DependencyDatabase):
    data = await get_available_lenders(database)
    return {
        "status" : "success",
        "lenders_data" : data
    }




@router.get("/archive")
async def get_archive_data(
    database : DependencyDatabase, 
    current_user : Annotated[User, Depends(get_current_user)]):
        data = await get_archived_loan(database, current_user.id)
        return {
            "status" : "success",
            "archive_data" : data
        }









