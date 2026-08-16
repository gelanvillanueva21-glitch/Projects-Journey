

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from app.models.task import Task
from app.schemas.task import TaskCreate, TaskUpdate


class TaskRepository:
    def __init__(self, db: AsyncSession):
        self.db = db


    async def get_all_by_owner(self, owner_id: int) -> list[Task]:
        result = await self.db.execute(select(Task).where(Task.owner_id == owner_id))
        return result.scalars().all()


    async def get_by_id(self, task_id: int, owner_id: int) -> Task | None:
        result = await self.db.execute(select(Task).where(
            Task.id == task_id,
            Task.owner_id == owner_id
            ))
        return result.scalar_one_or_none()


    async def create(self, data: TaskCreate, owner_id: int) -> Task:
        task = Task(**data.model_dump(), owner_id=owner_id)
        self.db.add(task)
        await self.db.commit()
        await self.db.refresh(task)
        return task


    async def update(self, task: Task, data: TaskUpdate) -> Task:
        update_data = data.model_dump(exclude_unset=True)
        for field, value in update_data.items():
            setattr(task, field, value)
        await self.db.commit()
        await self.db.refresh(task)
        return task


    async def delete(self, task: Task) -> None:
        await self.db.delete(task)
        await self.db.commit()




