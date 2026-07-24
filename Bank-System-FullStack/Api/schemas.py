from pydantic import BaseModel, EmailStr, Field, ConfigDict
from typing import Annotated



class UserBase(BaseModel):
    email : EmailStr



class CreateUser(UserBase):
    password : Annotated[str, Field(min_length = 8, max_length = 50)]


class UserResponse(BaseModel):
    id : int
    email : EmailStr
    is_active : Annotated[bool, Field(default = True)]
    
    model_config = ConfigDict(from_attributes = True)



