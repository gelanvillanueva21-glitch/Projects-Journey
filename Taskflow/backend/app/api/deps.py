
from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession
from app.core.database import get_db
from app.repositories.task import TaskRepository
from typing import Annotated



async def get_task_repo(db: Annotated[AsyncSession, Depends(get_db)]) -> TaskRepository:
    return TaskRepository(db)



