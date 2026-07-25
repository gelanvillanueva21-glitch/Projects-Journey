from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, update
from models import User, Loan, LoanPayment, Withdraw, Deposit
from schemas import CreateUser, DepositMoney, WithdrawMoney, LaonMoney
from datetime import datetime, timezone
from auth import hash_password



async def get_user_email(
    database : AsyncSession,
    email : str
) -> User:
        data = await database.execute(select(User).where(
            User.email == email))
        return data.scalar_one_or_none()



async def create_user_account(
    database : AsyncSession,
    user : CreateUser
) -> User:
        hashed_password = hash_password(user.password)
        user_data = User(
            email = user.email,
            hashed_password = hashed_password
        )
        database.add(user_data)
        await database.commit()
        await database.refresh(user_data)
        return user_data



async def borrow_money(
    database : AsyncSession,
    loan : LaonMoney,
    deptor_id : int,
    lender_id : int
) -> Loan:
        result = check_loaned_exist(database, deptor_id, lender_id)
        if not result:
            return None
        
        
        
        borrowed_data = Loan(
            deptor_id = deptor_id,
            lender_id = lender_id,
            due_date = loan.due_date,
            monthly_due_date = loan.monthly_due_date,
            loan_balance = loan.loan_value,
            anual_interest_rate = loan.anual_interest_rate
        )
        database.add(borrowed_data)
        await database.commit()
        await database.refresh(borrowed_data)
        return borrowed_data



async def payment(
    database : AsyncSession,
    user_payment : LaonMoney,
    deptor_id : int,
    lender_id : int
) -> LoanPayment:
        data_payment = LoanPayment(
            paid_amount = user_payment.loan_value
        )



async def check_loaned_exist(
    database : AsyncSession,
    deptor_id : int,
    lender_id : int):
        result = await database.execute(select(Loan).where(
            Loan.debtor_id == deptor_id,
            Loan.lender_id == lender_id))
        return result.scalar_one_or_none()



async def check_due_date(
    database : AsyncSession,
    deptor_id : int,
    lender_id : int) -> bool:
        result = await database.execute(select(Loan).where(
            Loan.deptor_id == deptor_id,
            Loan.lender_id == lender_id))
        data = result.scalar_one_or_none()
        date_now = datetime.now(timezone.utc)
        
        if data.monthly_due_date:
            pass
        
        if data.due_date:
            return data.due_date > date_now




