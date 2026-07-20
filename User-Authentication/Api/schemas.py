from pydantic import BaseModel, EmailStr, Field
from typing import Annotated


class UserBase(BaseModel):
    email : EmailStr


class UserCreate(UserBase):
    password : Annotated[str, Field(min_length = 8, max_length = 50)]


class UserResponse(BaseModel):
    id : int
    is_active : bool
    
    class Config:
        from_attributes = True


class TaskBase(BaseModel):
    title : Annotated[str, Field(min_lenght = 1, max_lenght = 255)]
    description : Annotated[str | None, Field(default = None, max_lenght = 500)]


class TaskCreate(TaskBase): pass
class TaskResponse(TaskBase):
    id : int
    is_done : bool
    user_id : int
    
    class Config:
        from_attributes = True


class Token(BaseModel):
    access_token : str
    token_type : str