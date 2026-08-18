
from fastapi import Depends, HTTPException, status, Request
from jose import jwt, JWTError
from sqlalchemy.ext.asyncio import AsyncSession


from app.core.database import get_db
from app.repositories.task import TaskRepository
from typing import Annotated
from app.core.config import settings
from app.repositories.user import UserRepository
from app.models.user import User



async def get_task_repo(db: Annotated[AsyncSession, Depends(get_db)]) -> TaskRepository:
    return TaskRepository(db)



async def get_user_repo(db: Annotated[AsyncSession, Depends(get_db)]) -> UserRepository:
    return UserRepository(db)



async def get_current_user(
    reqeust: Request,
    db: Annotated[AsyncSession, Depends(get_db)]
) -> User:
        token = reqeust.cookies.get("access_token")
        if not token:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Not authenticated"
            )
        try:
            payload = jwt.decode(
                token,
                settings.SECRET_KEY,
                algorithms=[settings.ALGORITHM]
            )
            user_id: str | None = payload.get("sub")
            if user_id is None:
                raise HTTPException(
                    status_code=status.HTTP_401_UNAUTHORIZED,
                    detail="Invalid token",
                )
        except JWTError:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid token",
            )

        user_repo = UserRepository(db)
        user = await user_repo.get_by_id(int(user_id))
        if user is None:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="User not found",
            )
        return user


