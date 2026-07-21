from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from typing import Annotated
from ..database import get_database
from ..schemas import TaskCreate, TaskResponse
from ..crud import create_task, get_users_task
from authentication import get_user
from ..models import User


router = APIRouter(
    prefix = "/Tasks",
    tags = ["Tasks"]
)


@router.get("/get-tasks", response_model = list[TaskResponse])
async def read_tasks(
    current_user : Annotated[User, Depends(get_user)],
    database : Annotated[AsyncSession, Depends(get_database)]):
        return await get_users_task(database, current_user.id)


@router.post(
    "/create-tasks", 
    response_model = TaskResponse,
    status_code = status.HTTP_201_CREATED)
async def create_task(
    task : TaskCreate,
    database : Annotated[AsyncSession, Depends(get_database)],
    current_user : Annotated[User, Depends(get_user)]):
        return await create_task(database, current_user.id)



