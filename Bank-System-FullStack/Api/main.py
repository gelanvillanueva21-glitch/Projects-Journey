from fastapi import FastAPI
from Router import deposit, authentication, withdraw, loan, users



app = FastAPI(title = "MyBank")
app.include_router(deposit.router)
app.include_router(authentication.router)
app.include_router(users.router)
app.include_router(withdraw.router)
app.include_router(loan.router)




