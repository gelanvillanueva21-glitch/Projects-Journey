
from datetime import datetime
from pydantic import BaseModel, ConfigDict


class TaskBase(BaseModel):
    title: str
    description: str | None = None
    completed: bool = False


class TaskCreate(TaskBase): pass


class TaskUpdate(TaskBase):
    title: str | None = None
    description: str | None = None
    completed: bool = False



class TaskResponse(TaskBase):
    model_config = ConfigDict(from_attributes=True)

    id: int
    created_at: datetime
    updated_at: datetime





