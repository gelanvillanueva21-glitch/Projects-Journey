from fastapi import FastAPI, HTTPException, status
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field, field_validator
from typing import Annotated
from database import UsersInfo
import re

userInfo = UsersInfo()
app = FastAPI()


# This allow us to connect our local backend and local frontend
# website to talk each other, I learned it from Gemini
app.add_middleware(
    CORSMiddleware,
    allow_origins = ["*"],
    allow_credentials = False,
    allow_methods = ["*"],
    allow_headers = ["*"]
)


class UserAuth(BaseModel):
    userId : Annotated[int, Field(
        gt = 99,
        le = 999999,
        description = "Id must greater than 99 and less than 999999"
    )]
    username : Annotated[str, Field(
        min_length = 3, 
        max_length = 50, 
        pattern = r"^[a-zA-Z0-9_-]+$",
        description = "3-20 characters. Only letters, numbers, underscores, or hyphens."
        )]
    password : str
    
    @field_validator('password')
    @classmethod
    def validate_password(cls, value : str):
        password_regex = r"^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[@$!%*?&])[A-Za-z\d@$!%*?&]{8,}$"
        
        if not re.match(password_regex, value):
            raise ValueError(
                "Password must be at least 8 characters long and include an "
                "uppercase letter, lowercase letter, number, and special character."
            )
        return value


@app.post("/Login")
async def logIn(user : UserAuth):
    if user.userId in userInfo.info:
        db_user = userInfo.info[user.userId]
        if user.username == db_user.get("Username") and user.password == db_user.get("Password"):
            return {
                "status" : "success",
                "todo_list" : db_user.get("To-Do-List", [])
            }
        raise HTTPException(status_code = status.HTTP_401_UNAUTHORIZED)
    else:
        raise HTTPException(status_code = status.HTTP_404_NOT_FOUND)
