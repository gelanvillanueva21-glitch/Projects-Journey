from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.ext.asyncio import AsyncSession
from pydantic import Field
from typing import Annotated
from Router.authentication import get_current_user, DependencyDatabase
from schemas import LoanMoney, LoanPay, LoanResponse
from models import LoanHistory, Loan, LoanPayment, User
from crud import get_archived_loan, borrow_money, payment, active_lend, lend_amount, get_available_lenders, deactive_lend, delete_archive_loan, get_current_loans, get_debtor_loan


router = APIRouter(prefix = "/loan", tags = ["loan"])



@router.post("/", response_model = LoanResponse)
async def borrow(
    database : DependencyDatabase,
    current_user : Annotated[User, Depends(get_current_user)],
    lender_user : int,
    loan : LoanMoney):
    """
    A post borrow function the get the lender user id 
    (to access and modefiy e.g. like chaging and adding),
    current user get from the get_current_user function,
    it gets the data of user when logging in through jwt
    """
    if current_user.id == lender_user:
        raise HTTPException(
            status_code = status.HTTP_400_BAD_REQUEST,
            detail = "You can not loan from yourself"
        )
    
    try:
        data = await borrow_money(database, loan, current_user.id, lender_user)
        if isinstance(data, str):
            raise HTTPException(
                status_code = status.HTTP_400_BAD_REQUEST,
                detail = data
            )
        await database.commit()
        await database.refresh(data)
        return {
            "loan_value" : data.loan_balance,
            "anual_interest_rate" : data.anual_interest_rate,
            "monthly_due_date" : data.monthly_due_date,
            "due_date" : data.due_date
        }
    except ValueError:
        await database.rollback()
        raise HTTPException(status_code = status.HTTP_400_BAD_REQUEST)


@router.post("/pay")
async def loan_payment(
    database : DependencyDatabase,
    payment_info : LoanPay,
    lender_user : int,
    current_user : Annotated[User, Depends(get_current_user)]):
        """
        A post loan payment function payment_info is a
        pydantic schemas that  a paid amoount, we get the
        lender user same reason for our borrow function
        to modefy some changes to it
        """
        
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
                detail = data if data else "Insufficient amount"
            )
        
        if isinstance(data, list):
            response_data = data[0]
            return {
                "status" : data[1],
                "new_amount" : response_data.loan_balance
            }
        await database.commit()
        await database.refresh(data)
        return {"paid_amount" : data.paid_amount}






@router.post("/activate")
async def activate_lender(
    database : DependencyDatabase,
    amount : Annotated[int, Query(ge=1000, le=10000)],
    interest_rate : Annotated[int, Query(ge=3, le=15)],
    current_user : Annotated[User, Depends(get_current_user)]):
        """
        A post activate lender to activate so other users
        can lend an amount of money with an interest rate
        we always use current_user to get the info throught
        jwt
        """
        
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
        try:
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
        """
        This post function let us deactivate meaning
        users are no longer can barrow money from you
        it deactivate by using the user id throught the function deactive_lend
        """
        
        result = await deactive_lend(database, current_user.id)
        if not result:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST)
        return {"status" : "success"}




@router.get("/debtor")
async def get_debtor(
    database : DependencyDatabase,
    current_user : Annotated[User, Depends(get_current_user)]):
        """
        A get function that lets us get the debtor who
        loan from you to know what there names
        """
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
    """
    A get function of getting the availabe person
    who can lend money, this always get whenever visiting
    the website from frontend
    """
    
    data = await get_available_lenders(database)
    return {
        "status" : "success",
        "lenders_data" : data
    }




@router.get("/archive")
async def get_archive_data(
    database : DependencyDatabase, 
    current_user : Annotated[User, Depends(get_current_user)]):
        """
        Another get function that get the archive you loan
        and already finished paid
        """
        
        data = await get_archived_loan(database, current_user.id)
        return {
            "status" : "success",
            "archive_data" : data
        }





@router.get("/current")
async def get_current_data_loan(
    database : DependencyDatabase,
    current_user : Annotated[User, Depends(get_current_user)]):
        """
        A get function that gets the name of you loan
        at, there are limits of how many you can barrow a
        money, which is 5
        """
        
        data = await get_current_loans(database, current_user.id)
        return {
            "status" : "success",
            "data" : data
        }




@router.delete("/archive/delete")
async def delete_archive_data(
    database : DependencyDatabase,
    current_user : Annotated[User, Depends(get_current_user)]):
        """
        A function that delete the archived data
        (a history you barrow money from)
        """
        
        result = await delete_archive_loan(database, current_user.id)
        if not result:
            raise HTTPException(
                status_code = status.HTTP_400_BAD_REQUEST,
                detail = "Archived history empty"
            )
        return {"status" : "success"}





