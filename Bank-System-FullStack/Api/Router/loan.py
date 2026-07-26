from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from typing import Annotated
from Router.authentication import get_current_user, DependencyDatabase
from schemas import LoanMoney, LoanPay, LoanRespons
from models import LoanHistory, Loan, LoanPayment, User
from crud import get_archived_loan, borrow_money, payment, active_lend, lend_amount, get_available_lenders



router = APIRouter(prefix = "/loan", tags = ["loan"])



@router.post("/", response_model = LoanRespons)
async def borrow(
    database : DependencyDatabase,
    current_user : Annotated[User, Depends(get_current_user)],
    lender_user : str,
    loan : LoanMoney):
    data = await borrow_money(database, loan, current_user.id, lender_user)
    if isinstance(data, str):
        raise HTTPException(
            status_code = status.HTTP_400_BAD_REQUEST,
            detail = data
        )
    return data



@router.post("/pay", response_model = LoanPayment)
async def loan_payment(
    database : DependencyDatabase,
    payment_info : LoanPay,
    lender_user : str,
    current_user : Annotated[User, Depends(get_current_user)]):
        data = await payment(
            database, 
            payment_info, 
            current_user.id, 
            lender_user)
        if isinstance(data, str) or data is None:
            raise HTTPException(
                status_code = status.HTTP_400_BAD_REQUEST,
                detail = data if data else "Error occured during payment request"
            )
        return data














