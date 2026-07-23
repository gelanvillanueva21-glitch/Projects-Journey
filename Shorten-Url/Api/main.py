from fastapi import FastAPI
from Router import authentication, redirect, url, users


app = FastAPI()


app.include_router(authentication.router)
app.include_router(redirect.router)
app.include_router(url.router)
app.include_router(users.router)




