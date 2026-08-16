

from fastapi import APIRouter, Depends, HTTPException, status
from app.repositories.task import TaskRepository
from app.schemas.task import TaskCreate, TaskUpdate, TaskResponse
from app.api.deps import get_task_repo, get_current_user
from app.models.user import User
from typing import Annotated


router = APIRouter(prefix="/tasks", tags=["tasks"])


@router.get("", response_model=list[TaskResponse])
async def list_tasks(
    repo: Annotated[TaskRepository, Depends(get_task_repo)],
    current_user: Annotated[User, Depends(get_current_user)]
):
    return await repo.get_all_by_owner(current_user.id)


@router.get("/{task_id}", response_model=TaskResponse)
async def get_task(
    task_id: int,
    repo: Annotated[TaskRepository, Depends(get_task_repo)],
    current_user: Annotated[User, Depends(get_current_user)]
):
    task = await repo.get_by_id(task_id, current_user.id)
    if not task:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Task with  id {task_id} not found"
        )
    return task



@router.post(
    "", 
    response_model=TaskResponse,
    status_code=status.HTTP_201_CREATED
)
async def create_task(
    data: TaskCreate,
    repo: Annotated[TaskRepository, Depends(get_task_repo)],
    current_user: Annotated[User, Depends(get_current_user)]
):
    return await repo.create(data, current_user.id)


@router.put(
    "/{task_id}",
    response_model=TaskResponse,
    )
async def update_task(
    task_id: int,
    data: TaskUpdate,
    repo: Annotated[TaskRepository, Depends(get_task_repo)],
    current_user: Annotated[User, Depends(get_current_user)]
):
    task = await repo.get_by_id(task_id, current_user.id)
    if not task:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Task with id {task_id} not found",
        )
    return await repo.update(task, data)


@router.delete(
    "/{task_id}",
    status_code=status.HTTP_204_NO_CONTENT
)
async def delete_task(
    task_id: int,
    repo: Annotated[TaskRepository, Depends(get_task_repo)],
    current_user: Annotated[User, Depends(get_current_user)]
):
    task = await repo.get_by_id(task_id, current_user.id)
    if not task:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Task with id {task_id} not found"
        )
    await repo.delete(task)
    return None


