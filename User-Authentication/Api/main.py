from fastapi import FastAPI
from Router import user, authentication, task


app = FastAPI(title = "MyApp")
app.include_router(user.router)
app.include_router(authentication.router)
app.include_router(task.router)