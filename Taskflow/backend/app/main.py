


from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy import text

from app.core.database import engine
from app.models import task, user # noqa: F401 -- registers model with Base.metadata
from app.api.v1 import tasks as tasks_router
from app.api.v1 import auth as auth_router



@asynccontextmanager
async def lifespan(app: FastAPI):
    async with engine.begin() as conn:
        await conn.execute(text("SELECT 1"))
    print("✅ Database connection established")
    yield
    await engine.dispose()
    print("🔌 Database connection closed")


app = FastAPI(title="Taskflow API", lifespan=lifespan)


app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)


app.include_router(tasks_router.router, prefix="/api/v1")
app.include_router(auth_router.router, prefix="/api/v1")


@app.get("/health")
async def health_check():
    return {
        "status": "ok",
        "message": "TaskFlow backend is running"
    }


