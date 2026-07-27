from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, update, delete
from models import User, Loan, LoanPayment, Withdraw, Deposit, LoanHistory
from schemas import CreateUser, LoanMoney, LoanPay
from datetime import datetime, timezone
from auth import hash_password
from hmac_auth import create_hmac


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
        hashed_pass = hash_password(user.password)
        user_data = User(
            email = user.email,
            hashed_password = hash_password,
            name = user.name
        )
        print(user_data)
        database.add(user_data)
        await database.commit()
        await database.refresh(user_data)
        return user_data



# A function to borrow money from lender using lender_id
# and getting the deptor id to save
async def borrow_money(
    database : AsyncSession,
    loan : LoanMoney,
    deptor_id : int,
    lender_id : int
) -> Loan:
        result = await check_loaned_exist(database, deptor_id, lender_id)
        if result:
            return "You have not fully paid yet"
        if await is_loaned_limit(database, deptor_id):
            return "Loan has reach to its maximum"
        
        borrowed_data = Loan(
            lender_id = lender_id,
            due_date = loan.due_date,
            monthly_due_date = loan.monthly_due_date,
            loan_balance = loan.loan_value,
            anual_interest_rate = loan.anual_interest_rate
        )
        
        data = await database.get(User, lender_id)
        if not data:
            return "Data not found"
        data.amount_lend -= loan.loan_value
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
            return "Loan did not exist"
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




# A function that activate lender so you can lend them
# a money
async def active_lend(
    database : AsyncSession,
    id : int):
    data = await database.get(User, id)
    if not data:
        return None
    data.can_lend = True
    await database.commit()
    return True




# A function that modefy how much can you lend to the user
async def lend_amount(
    database : AsyncSession,
    id : int,
    amount : int):
    data = await database.get(User, id)
    if data.can_lend:
        if amount > 100 and amount < 10000 and data.availabe_balance > amount:
            data.amount_lend += amount
            data.availabe_balance -= amount
    await database.commit()
    await database.refresh(data)
    return data




# A function to get the archived loan history
async def get_archived_loan(
    database : AsyncSession,
    user_id : int) -> list:
        data = await database.execute(select(LoanHistory).where(LoanHistory.deptor_id == user_id))
        result = await database.stream_scalars(data)
        if result:
            output_list = []
            async for info in result:
                loan_info = {
                    "id" : info.id,
                    "deptor_id" : info.deptor_id,
                    "lender_id" : info.lender_id,
                    "paid_date" : info.paid_date,
                    "complete_paid" : info.is_paid
                }
                output_list.append(loan_info)
            return output_list
        return output_list




# A function that will return all the user
# that is available to lend a loan
async def get_available_lenders(database : AsyncSession):
    data = database.execute(select(User).where(
        User.can_lend == True,
        User.availabe_balance >= 1000
    ))
    result = await database.stream_scalars(data)
    output_list = []
    async for user in result:
        output_list.append([{
            "id" : user.id,
            "name" : user.name,
            "active" : user.is_acitve,
            "interest" : user.anual_interest_rate,
            "available_lend_amount" : user.amount_lend,
            "created_at" : user.created_at,
            "hmac_signature" : create_hmac(str(user.id).encode("utf-8"))
        }])
    return output_list






# A function to withdraw amount if the balance is
# still sufficient
async def withdraw(
    database : AsyncSession,
    user_id : int,
    amount : int
) -> Withdraw | None:
        response = await database.execute(select(User).where(
            User.id == user_id))
        data = response.scalar_one_or_none()
        if data.availabe_balance > amount:
            data.availabe_balance -= amount
            withdraw_data = Withdraw(withdraw_amount = amount)
            database.add(withdraw_data)
            await database.commit()
            await database.refresh(data)
            await database.refresh(withdraw_data)
        return withdraw_data




# A function that will get every withdraw
# of the users
async def get_withdraws(
    database : AsyncSession,
    user_id : int) -> list:
        data = await database.execute(select(Withdraw).where(Withdraw.user_id == user_id))
        result = await database.stream_scalars(data)
        output_list = []
        if result:
            for info in result:
                data_info = {
                    "withdraw_amount" : info.withdraw_amount,
                    "withdraw_date" : info.date
                }
                output_list.append([data_info])
            return output_list
        return output_list




# A function to deposit a balance to the database
async def deposit(
    database : AsyncSession,
    user_id : int,
    amount : int) -> Deposit | None:
        response = await database.execute(select(User).where(User.id == user_id))
        data = response.scalar_one_or_none()
        if data:
            data.availabe_balance += amount
            await database.commit()
            await database.refresh()
        return data




# A function that will get the history
# of deposit user
async def get_deposits(
    database : AsyncSession,
    user_id : int) -> list:
        data = await database.execute(select(Deposit).where(Deposit.user_id == user_id))
        result = await database.stream_scalars(data)
        output_list = []
        if result:
            for info in result:
                data_info = {
                    "deposit_amount" : info.deposit_amount,
                    "deposit_date" : info.date
                }
            return output_list
        return output_list





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



# A helper function to check if the balance is
# zero if it does zero delete the data inside the database
async def check_loan_balance(
    database : AsyncSession,
    loan : Loan,
    deptor_id : int,
    lender_id : int):
    if loan.loan_balance == 0:
        delete_row_loan = await database.execute(select(Loan).where(
            Loan.debtor_id == deptor_id,
            Loan.lender_id == lender_id
        ))
        data = delete_row_loan.scalar_one_or_none()
        archived_loan = LoanHistory(lender_id = data.lender_id)
        database.add(archived_loan)
        await database.delete(delete_row_loan)
        await database.commit()
        await database.refresh(archived_loan)




# A helper function to see if the user already
# maximum the loaned
async def is_loaned_limit(
    database : AsyncSession,
    deptor_id : int) -> bool:
        data = await database.execute(select(Loan).where(Loan.deptor_id == deptor_id,))
        data = data.scalars().all()
        if len(data) == 5:
            return True
        return False











