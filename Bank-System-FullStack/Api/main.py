from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from Router import deposit, authentication, withdraw, loan, users




app = FastAPI(title = "MyBank")
app.add_middleware(
    CORSMiddleware,
    allow_origins = ["*"],
    allow_credentials = False,
    allow_methods = ["*"],
    allow_headers = ["*"]
)



app.include_router(deposit.router)
app.include_router(authentication.router)
app.include_router(users.router)
app.include_router(withdraw.router)
app.include_router(loan.router)




