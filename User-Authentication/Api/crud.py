from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from models import User, Task
from schemas import UserCreate, TaskCreate
from auth import hash_password


async def get_user_email(
    database : AsyncSession,
    email : str) -> User | None:
        result = await database.execute(select(User).where(User.email == email))
        return result.scalar_one_or_none()


async def create_user(
    database : AsyncSession,
    user : UserCreate) -> User:
        hashed_pass = hash_password(user.password)
        data_user = User(email=user.email, hashed_password = hashed_pass)
        database.add(data_user)
        print(data_user)
        await database.commit()
        await database.refresh(data_user)
        return data_user


async def get_users_task(
    database : AsyncSession,
    user_id : int) -> list[Task]:
        result = await database.execute(select(Task).where(Task.user_id == user_id))
        return result.scalars().all()



async def create_task(
    database : AsyncSession,
    task : TaskCreate,
    user_id : int) -> Task:
        data_task = Task(
            title = task.title,
            description = task.description,
            user_id = user_id
        )
        database.add(data_task)
        await database.commit()
        await database.refresh(data_task)
        return data_task

