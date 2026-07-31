from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, update, delete
from models import User, Loan, LoanPayment, Withdraw, Deposit, LoanHistory
from schemas import CreateUser, LoanMoney, LoanPay
from datetime import datetime, timezone, timedelta
from dateutil.relativedelta import relativedelta
from auth import hash_password, verify_password


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
            hashed_password = hashed_pass,
            name = user.name
        )
        database.add(user_data)
        await database.commit()
        await database.refresh(user_data)
        return user_data




# A function to change password on a specific account
async def change_user_password(
    database : AsyncSession,
    current_password : str,
    new_hashed_password : str,
    user_account : User) -> bool:
        is_pass_same = verify_password(current_password, user_account.hashed_password)
        if not is_pass_same:
            return False
        user_account.hashed_password = new_hashed_password
        await database.commit()
        return True




# A function to borrow money from lender using lender_id
# and getting the deptor id to save
async def borrow_money(
    database : AsyncSession,
    loan : LoanMoney,
    debtor_id : int,
    lender_id : int
) -> Loan | str:
        result = await check_loaned_exist(database, debtor_id, lender_id)
        lender_data = await is_lender_exist(database, lender_id)
        if not lender_data:
            return "Lender does not exist"
        if not await is_lender_can_lend(database, lender_id):
            return "Lender is not available"
        if not await is_lender_enough_balance(database,lender_id, loan.loan_value):
            return "Lender balance insufficient"
        if result:
            return "You have not fully paid yet"
        if await is_loaned_limit(database, debtor_id):
            return "Loan has reach to its maximum"
            
        total_amount = anual_interest_calculation(loan.loan_value, lender_data.anual_interest_rate)
        borrowed_data = Loan(
            debtor_id = debtor_id,
            lender_id = lender_id,
            due_date = loan.due_date,
            monthly_due_date = loan.monthly_due_date,
            loan_balance = total_amount,
            anual_interest_rate = lender_data.anual_interest_rate
        )
        await helper_borrow_function(database, debtor_id, lender_id, loan.loan_value)
        database.add(borrowed_data)
        return borrowed_data



# A payment function saving in the database while updating
# the total amount in the database
async def payment(
    database : AsyncSession,
    user_payment : LoanPay,
    debtor_id : int,
    lender_id : int):
        data = await check_loaned_exist(database, debtor_id, lender_id)
        if not data:
            return "Loan did not exist"
        if is_overdue(data.due_date if data.due_date else data.monthly_due_date):
            data.loan_balance = anual_interest_calculation(data.loan_balance, 1)
            
            if data.due_date:
                data.due_date = datetime.now(timezone.utc).replace(tzinfo=None) + timedelta(days=5)
            else:
                data.monthly_due_date = datetime.now(timezone.utc).replace(tzinfo=None) + timedelta(days=5)
            await database.commit()
            await database.refresh(data)
            return [data, "Your payment is past due. A 1 percent late fee has been applied to your total."]
        is_accepted = False
        payment = None
        if data.monthly_due_date:
            if user_payment.paid_amount == (data.loan_balance // data.monthly_pay):
                payment = LoanPayment(
                    debtor_id = debtor_id,
                    lender_id = lender_id,
                    paid_amount = user_payment.paid_amount
                )
                data.monthly_due_date = data.monthly_due_date.replace(tzinfo=None) + relativedelta(months=1)
                data.monthly_pay -= 1
                is_accepted = True
        if data.due_date:
            if user_payment.paid_amount == data.loan_balance:
                payment = LoanPayment(
                    debtor_id = debtor_id,
                    lender_id = lender_id,
                    paid_amount = user_payment.paid_amount
                )
                is_accepted = True
        if is_accepted:
            loan_info = await decreas_amount(database, data, user_payment.paid_amount, debtor_id, lender_id)
            await check_loan_balance(database, loan_info, debtor_id, lender_id)
        if payment is not None:
            database.add(payment)
        return payment




# A function that activate lender so you can lend them
# a money
async def active_lend(
    database : AsyncSession,
    id : int):
    data = await database.get(User, id)
    if not data:
        return False
    data.can_lend = True
    return True



# A function that deactivate lender
async def deactive_lend(
    database : AsyncSession,
    id : int):
    data = await database.get(User, id)
    if not data:
        return None
    if data.can_lend:
        data.can_lend = False
        data.available_balance += data.amount_lend
        data.anual_interest_rate = 0
        data.amount_lend = 0
        return True
    return None







# A function that modefy how much can you lend to the user
async def lend_amount(
    database : AsyncSession,
    id : int,
    amount : int,
    interest : int):
    data = await database.get(User, id)
    if data.can_lend:
        if amount >= 100 and amount <= 10000 and data.available_balance >= amount:
            if data.anual_interest_rate == 0:
                data.anual_interest_rate += interest
            data.amount_lend += amount
            data.available_balance -= amount
            return data
    return None




# A function that will delete archive loan data
# in database
async def delete_archive_loan(
    database : AsyncSession,
    id : int):
    data = await database.execute(delete(LoanHistory).where(LoanHistory.debtor_id == id))
    await database.commit()
    return True




# A function to get the archived loan history
async def get_archived_loan(
    database : AsyncSession,
    user_id : int) -> list[LoanHistory]:
        data = await database.execute(select(LoanHistory).where(LoanHistory.debtor_id == user_id))
        result = data.scalars().all()
        output_list = []
        if len(result) != 0:
            for info in result:
                output_list.append({
                    "debtor_id" : info.debtor_id,
                    "lender_id" : info.lender_id,
                    "is_paid" : info.is_paid,
                    "date" : info.paid_date
                })
        return output_list





# A function to get the users who borrowed money from current user
async def get_debtor_loan(
    database : AsyncSession,
    user_id : int):
    data = await database.execute(select(Loan).where(Loan.lender_id == user_id))
    response_data = data.scalars().all()
    output_list = []
    if len(response_data) != 0:
        for info in response_data:
            user_data = await database.get(User, info.debtor_id)
            output_list.append({
                "debtor_id" : info.debtor_id,
                "name" : user_data.name,
                "loaned_date" : info.loaned_date,
                "due_date" : info.due_date if info.due_date else info.monthly_due_date,
                "loan_balance" : info.loan_balance,
                "anual_interest_rate" : info.anual_interest_rate
            })
    return output_list




# A function that will return all the user
# that is available to lend a loan
async def get_available_lenders(database : AsyncSession):
    data = await database.execute(select(User).where(
        User.can_lend == True,
        User.amount_lend >= 1000
    ))
    result = data.scalars().all()
    output_list = []
    if len(result) != 0:
        for info in result:
            output_list.append({
                "id" : info.id,
                "name" : info.name,
                "amount_lend" : info.amount_lend,
                "is_active" : info.is_active,
                "anual_interest_rate" : info.anual_interest_rate
            })
    return output_list





# A function that will return current loan that user has
async def get_current_loans(
    database : AsyncSession,
    id : int):
        data = await database.execute(select(Loan).where(Loan.debtor_id == id))
        result = data.scalars().all()
        output_list = []
        if len(result) != 0:
            for info in result:
                output_list.append({
                    "lender_id" : info.lender_id,
                    "loaned_date" : info.loaned_date,
                    "pay_date" : info.due_date if info.due_date is not None else info.monthly_due_date,
                    "loan_balance" : info.loan_balance
                })
        return output_list





# A function to withdraw amount if the balance is
# still sufficient
async def withdraw(
    database : AsyncSession,
    user_id : int,
    amount : int
) -> Withdraw | None:
        data = await database.get(User, user_id)
        withdraw_data = None
        if data.available_balance >= amount:
            data.available_balance -= amount
            withdraw_data = Withdraw(
                user_id = user_id,
                withdraw_amount = amount)
            database.add(withdraw_data)
            await database.commit()
            await database.refresh(data)
            await database.refresh(withdraw_data)
        return withdraw_data




# A function that will get every withdraw
# of the users
async def get_withdraws(
    database : AsyncSession,
    user_id : int) -> list[Withdraw]:
        data = await database.execute(select(Withdraw).where(Withdraw.user_id == user_id))
        result = data.scalars().all()
        output_list = []
        if len(result) != 0:
            for info in result:
                output_list.append({
                    "withdraw_amount" : info.withdraw_amount,
                    "date" : info.date
                })
        return output_list




# A function that delete deposits history
async def delete_withdraw_histories(
    database : AsyncSession,
    id : int):
    data = await database.execute(delete(Withdraw).where(Withdraw.user_id == id))
    await database.commit()
    return True




# A function to deposit a balance to the database
async def deposit(
    database : AsyncSession,
    user_id : int,
    amount : int):
        await database.execute(
            update(User)
            .where(User.id == user_id)
            .values(available_balance = User.available_balance + amount))
        deposit_data = Deposit(
            user_id = user_id,
            deposit_balance = amount)
        database.add(deposit_data)
        await database.commit()
        return await get_balance(database, user_id)




# A function that will get the history
# of deposit user
async def get_deposits(
    database : AsyncSession,
    user_id : int) -> list[Deposit]:
        data = await database.execute(select(Deposit).where(Deposit.user_id == user_id))
        result = data.scalars().all()
        output_list = []
        if len(result) != 0:
            for info in result:
                output_list.append({
                    "deposit_amount" : info.deposit_balance,
                    "date" : info.date
                })
        return output_list





# A function that delete the users deposit history
async def delete_deposits_data(
    database : AsyncSession,
    id : int):
        data = await database.execute(delete(Deposit).where(Deposit.user_id == id))
        await database.commit()
        return True






# HELPER FUNCTIONS


# A helper function to check if the loaned already exist
# and sending the info from database aswell
async def check_loaned_exist(
    database : AsyncSession,
    debtor_id : int,
    lender_id : int):
        result = await database.execute(select(Loan).where(
            Loan.debtor_id == debtor_id,
            Loan.lender_id == lender_id))
        return result.scalar_one_or_none()



# A helpder function to check if the due date
# is already passed
def is_overdue(due_date : datetime) -> bool:
    if due_date.tzinfo is None:
        due_date = due_date.replace(tzinfo=timezone.utc)
    return datetime.now(timezone.utc) > due_date




# A helper function to calculate how much must be the
# payment to pay
def anual_interest_calculation(
    loan_amount : int,
    anual_interest_rate : int):
        total_payment = loan_amount
        interest_rate = anual_interest_rate
        return int(total_payment * (1 + interest_rate / 100))



# A helper function to decreas total amount of loan
async def decreas_amount(
    database : AsyncSession,
    loan : Loan,
    amount : int,
    user_id : int,
    lender_id : int):
        if loan:
            user_data = await database.get(User, user_id)
            lender_data = await database.get(User, lender_id)
            if user_data.available_balance < amount:
                raise ValueError("Balance insufficient")
            user_data.available_balance -= amount
            if lender_data.can_lend:
                lender_data.amount_lend += amount
            else:
                lender_data.available_balance += amount
            loan.loan_balance -= amount
            return loan



# A helper function to check if the balance is
# zero if it does zero delete the data inside the database
async def check_loan_balance(
    database : AsyncSession,
    loan : Loan,
    debtor_id : int,
    lender_id : int):
    if loan.loan_balance == 0:
        await database.delete(loan)
        archived_loan = LoanHistory(
            debtor_id = debtor_id,
            lender_id = lender_id)
        database.add(archived_loan)
        return True
    return False




# A helper function to see if the user already
# maximum the loaned
async def is_loaned_limit(
    database : AsyncSession,
    debtor_id : int) -> bool:
        data = await database.execute(select(Loan).where(Loan.debtor_id == debtor_id,))
        data = data.scalars().all()
        if len(data) == 5:
            return True
        return False




# A helper function to get the current amount of the account
async def get_balance(
    database : AsyncSession,
    user_id : int):
    data = await database.get(User, user_id)
    return data.available_balance





# A helper function to decrease the balance loan in at lender user
# at the same time increasing debtor user balance amount
async def helper_borrow_function(
    database : AsyncSession,
    user_id : int,
    lender_id : int,
    amount : int):
        user_data = await database.get(User, user_id)
        lender_data = await database.get(User, lender_id)
        if lender_data.amount_lend < amount:
            raise ValueError("Error occured during calculation amount balance")
        user_data.available_balance += amount
        lender_data.amount_lend -= amount
    




# A helper function to check if loan can lend
async def is_lender_can_lend(
    database : AsyncSession,
    lender_id : int) -> bool:
    data = await database.get(User, lender_id)
    return data.can_lend




# A helper function that check if the lender has
# enough balance to lend
async def is_lender_enough_balance(
    database : AsyncSession,
    lender_id : int,
    amount : int) -> bool:
        data = await database.get(User, lender_id)
        return data.amount_lend >= amount




# A helper function that check if lender exist
async def is_lender_exist(
    database : AsyncSession,
    lender_id : int):
    data = await database.get(User, lender_id)
    return data





