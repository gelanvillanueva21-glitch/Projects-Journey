from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, update, delete
from models import User, Loan, LoanPayment, Withdraw, Deposit
from schemas import CreateUser, DepositMoney, WithdrawMoney, LaonMoney, LoanPay
from datetime import datetime, timezone
from auth import hash_password


# A function that gets an info in database table using email
async def get_user_email(
    database : AsyncSession,
    email : str
) -> User:
        data = await database.execute(select(User).where(
            User.email == email))
        return data.scalar_one_or_none()



# A function to create email and returning a User attributes
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



# A function to borrow money from lender using lender_id
# and getting the deptor id to save
async def borrow_money(
    database : AsyncSession,
    loan : LaonMoney,
    deptor_id : int,
    lender_id : int
) -> Loan:
        result = await check_loaned_exist(database, deptor_id, lender_id)
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



# A payment function saving in the database while updating
# the total amount in the database
async def payment(
    database : AsyncSession,
    user_payment : LoanPay,
    deptor_id : int,
    lender_id : int
) -> LoanPayment | str | None:
        data = await check_loaned_exist(database, deptor_id, lender_id)
        if not data:
            return None
        if not await check_due_date(database, deptor_id, lender_id):
            increament_interest_rate(database, deptor_id, lender_id)
            return "Your payment is past due. A 1 percent late fee has been applied to your total."

        payment_amount = await anual_interest_calculation(database, deptor_id, lender_id)
        payment = None
        if data.monthly_due_date:
            if user_payment.amount == payment_amount:
                payment = LoanPayment(
                    deptor_id = deptor_id,
                    lender_id = lender_id,
                    paid_amount = user_payment.amount
                )
        if data.due_date:
            if user_payment.amount == payment_amount:
                payment = LoanPayment(
                    deptor_id = deptor_id,
                    lender_id = lender_id,
                    paid_amount = user_payment.amount
                )
        loan_info = await decreas_amount(database, data, user_payment.amount)
        check_loan_balance(database, loan_info, deptor_id, lender_id)
        database.add(payment)
        await database.commit()
        await database.refresh(payment)
        return payment




# A function to withdraw amount if the balance is
# still sufficient
async def withdraw(
    database : AsyncSession,
    withdraw_data : WithdrawMoney
) -> Withdraw:
        response = await database.execute(select(User).where(
            User.id == withdraw_data.id))
        data = response.scalar_one_or_none()
        if data.availabe_balance > withdraw_data.amount:
            data.availabe_balance -= withdraw_data.amount
            await database.commit()
            await database.refresh(data)
        return data




async def deposit(
    database : AsyncSession,
    deposit_data : DepositMoney
) -> Deposit:
        response = await database.execute(select(User).where(
            User.id == deposit_data.id
        ))
        data = response.scalar_one_or_none()
        if data:
            data.availabe_balance += deposit_data.amount
            await database.commit()
            await database.refresh()
        return data




# HELPER FUNCTIONS


# A helper function to check if the loaned already exist
# and sending the info from database aswell
async def check_loaned_exist(
    database : AsyncSession,
    deptor_id : int,
    lender_id : int):
        result = await database.execute(select(Loan).where(
            Loan.debtor_id == deptor_id,
            Loan.lender_id == lender_id))
        return result.scalar_one_or_none()



# A helpder function to check if the due date
# is already passed
async def check_due_date(
    database : AsyncSession,
    deptor_id : int,
    lender_id : int) -> bool:
        result = await database.execute(select(Loan).where(
            Loan.deptor_id == deptor_id,
            Loan.lender_id == lender_id))
        data = result.scalar_one_or_none()
        
        if data.monthly_due_date:
            month = datetime.now().month
            day = datetime.now().day
            return data.monthly_due_date.day >= day and data.monthly_due_date.month >= month
        
        if data.due_date:
            date_now = datetime.now(timezone.utc)
            return data.due_date > date_now




# A helper function to calculate how much must be the
# payment to pay
async def anual_interest_calculation(
    database : AsyncSession,
    deptor_id : int,
    lender_id : int):
        result = await check_loaned_exist(database, deptor_id, lender_id)
        if not result:
            return None
        
        total_payment = result.loan_balance
        interest_rate = result.anual_interest_rate
        if result.monthly_due_date:
            monthly_payment = (total_payment * (1 + interest_rate / 100)) / 12
            return monthly_payment
        
        if result.due_date:
            return (total_payment * (1 + interest_rate / 100))



# A helper function to increament the interest rate if the
# due date of the payment is passed
async def increament_interest_rate(
    database : AsyncSession,
    deptor_id : int,
    lender_id : int):
        increament_interest = await database.execute(
            update(Loan)
            .where(
                Loan.debtor_id == deptor_id,
                Loan.lender_id == lender_id
            ).values(anual_interest_rate = Loan.anual_interest_rate + 1)
        )
        await database.commit()
        await database.refresh(increament_interest)
        return increament_interest



# A helper function to decreas total amount of loan
async def decreas_amount(
    database : AsyncSession,
    loan : Loan,
    amount : int):
    if loan:
        loan.loan_balance -= amount
        await database.commit()
        return loan



async def check_loan_balance(
    database : AsyncSession,
    loan : Loan,
    deptor_id : int,
    lender_id : int):
    if loan.loan_balance <= 0:
        delete_row_loan = await database.execute(delete(Loan).where(
            Loan.debtor_id == deptor_id,
            Loan.lender_id == lender_id
        ))
        await database.commit()







