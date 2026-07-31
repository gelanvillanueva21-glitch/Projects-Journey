from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.ext.asyncio import AsyncSession
from pydantic import Field
from typing import Annotated
from Router.authentication import get_current_user, DependencyDatabase
from schemas import LoanMoney, LoanPay, LoanRespons
from models import LoanHistory, Loan, LoanPayment, User
from crud import get_archived_loan, borrow_money, payment, active_lend, lend_amount, get_available_lenders, deactive_lend, delete_archive_loan, get_current_loans, reset_lend_amount, reset_interest_rate, get_debtor_loan


router = APIRouter(prefix = "/loan", tags = ["loan"])



@router.post("/", response_model = LoanRespons)
async def borrow(
    database : DependencyDatabase,
    current_user : Annotated[User, Depends(get_current_user)],
    lender_user : int,
    loan : LoanMoney):
    try:
        if current_user.id == lender_user:
            raise HTTPException(
                status_code = status.HTTP_400_BAD_REQUEST,
                detail = "You can not loan from yourself"
            )
        data = await borrow_money(database, loan, current_user.id, lender_user)
        if isinstance(data, str):
            raise HTTPException(
                status_code = status.HTTP_400_BAD_REQUEST,
                detail = data
            )
        return {
            "loan_value" : data.loan_balance,
            "anual_interest_rate" : data.anual_interest_rate,
            "monthly_due_date" : data.monthly_due_date,
            "due_date" : data.due_date
        }
    except ValueError:
        await database.rollback()
        raise HTTPException(status_code = status.HTTP_400_BAD_REQUEST)


@router.post("/pay", response_model = LoanPay)
async def loan_payment(
    database : DependencyDatabase,
    payment_info : LoanPay,
    lender_user : int,
    current_user : Annotated[User, Depends(get_current_user)]):
        if current_user.id == lender_user:
            raise HTTPException(
                status_code = status.HTTP_403_FORBIDDEN,
                detail = "You can not pay or loan your own Account"
            )
        if current_user.available_balance < payment_info.paid_amount:
            raise HTTPException(
                status_code = status.HTTP_400_BAD_REQUEST,
                detail = "Insuficient balance to pay"
            )
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





@router.post("/reset_lender")
async def reset_lend(
    database : DependencyDatabase,
    current_user : Annotated[User, Depends(get_current_user)]):
        try:
            data = await reset_lend_amount(database, current_user.id)
            await database.commit(data)
            return {"status" : "success"}
        except Exception:
            await database.rollback()
            raise HTTPException(
                status_code = status.HTTP_400_BAD_REQUEST,
                detail = "Unexpected error occured"
            )




@router.post("/reset_interest")
async def reset_interest(
    database : DependencyDatabase,
    current_user : Annotated[User, Depends(get_current_user)]):
        try:
            data = await reset_interest_rate(database, current_user.id)
            if not data:
                raise HTTPException(
                    status_code = status.HTTP_400_BAD_REQUEST,
                    detail = "Can not reset interest, Users who loaned must pay first"
                )
        except Exception:
            await database.rollback()
            raise HTTPException(status_code = status.HTTP_400_BAD_REQUEST)




@router.post("/activate")
async def activate_lender(
    database : DependencyDatabase,
    amount : Annotated[int, Query(ge=1000, le=10000)],
    interest_rate : Annotated[int, Query(ge=3, le=15)],
    current_user : Annotated[User, Depends(get_current_user)]):
        try:
            if current_user.can_lend:
                raise HTTPException(
                    status_code = status.HTTP_403_FORBIDDEN,
                    detail = "Lender already activate"
                )
            result = await active_lend(database, current_user.id)
            if not result:
                raise HTTPException(status_code = status.HTTP_400_BAD_REQUEST)
            data = await lend_amount(database, current_user.id, amount, interest_rate)
            if not data:
                raise HTTPException(
                    status_code = status.HTTP_400_BAD_REQUEST,
                    detail = "Insufficient balance"
                )
            await database.commit()
            return {"status" : "success"}
        except Exception:
            await database.rollback()
            raise HTTPException(
                status_code = status.HTTP_400_BAD_REQUEST,
                detail = "Unexpected error occured"
            )




@router.post("/deactivate")
async def deactivate_lender(
    database : DependencyDatabase,
    current_user : Annotated[User, Depends(get_current_user)]):
        result = await deactive_lend(database, current_user.id)
        if not result:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST)
        return {"status" : "success"}




@router.get("/debtor")
async def get_debtor(
    database : DependencyDatabase,
    current_user : Annotated[User, Depends(get_current_user)]):
        try:
            data = await get_debtor_loan(database, current_user.id)
            return {
                "status" : "success",
                "data" : data
            }
        except Exception:
            raise HTTPException(
                status_code = status.HTTP_404_NOT_FOUND
            )




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





@router.get("/current")
async def get_current_data_loan(
    database : DependencyDatabase,
    current_user : Annotated[User, Depends(get_current_user)]):
        data = await get_current_loans(database, current_user.id)
        return {
            "status" : "success",
            "data" : data
        }




@router.delete("/archive/delete")
async def delete_archive_data(
    database : DependencyDatabase,
    current_user : Annotated[User, Depends(get_current_user)]):
        result = await delete_archive_loan(database, current_user.id)
        if not result:
            raise HTTPException(
                status_code = status.HTTP_400_BAD_REQUEST,
                detail = "Archived history empty"
            )
        return {"status" : "success"}





