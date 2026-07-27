import asyncio
from database import engine, Base
from models import Deposit, User, Withdraw, Loan, LoanHistory, LoanPayment



async def create_tables():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)



if __name__ == "__main__":
    asyncio.run(create_tables())
    print("Table created")




