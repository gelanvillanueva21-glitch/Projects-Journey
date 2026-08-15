


from contextlib import asynccontextmanager
from fastapi import FastAPI
from sqlalchemy import text
from app.core.database import engine
from app.models import task # noqa: F401 -- registers model with Base.metadata


@asynccontextmanager
async def lifespan(app: FastAPI):
    async with engine.begin() as conn:
        await conn.execute(text("SELECT 1"))
    print("✅ Database connection established")
    yield
    await engine.dispose()
    print("🔌 Database connection closed")


app = FastAPI(title="Taskflow API")



@app.get("/health")
async def health_check():
    return {
        "status": "ok",
        "message": "TaskFlow backend is running"
    }


