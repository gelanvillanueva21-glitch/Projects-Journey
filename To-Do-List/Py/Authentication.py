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
        le = 100000000000,
        description = "Id must greater than 99 and less than or equal 100,000,000,000"
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

class UpdateList(BaseModel):
    todo_list : Annotated[list[str], Field(default_factory = list)]
    deleted_list : str
    id : int

class AddItemList(BaseModel):
    item : Annotated[str, Field(max_length = 35)]
    id : int


@app.post("/Login")
async def logIn(user : UserAuth):
    if user.userId in userInfo.info:
        db_user = userInfo.info[user.userId]
        tempId = user.userId
        if user.username == db_user.get("Username") and user.password == db_user.get("Password"):
            return {
                "status" : "success",
                "todo_list" : db_user.get("To-Do-List", [])
            }
        raise HTTPException(status_code = status.HTTP_401_UNAUTHORIZED)
    else:
        raise HTTPException(status_code = status.HTTP_404_NOT_FOUND)


@app.post("/AddItem")
async def addItem(data : AddItemList):
    if not data.item:
        raise HTTPException(status_code = status.HTTP_406_NOT_ACCEPTABLE)
    
    if len(userInfo.info[data.id]["To-Do-List"]) >= 50:
        raise HTTPException(status_code = status.HTTP_403_FORBIDDEN)
    
    userInfo.info[data.id]["To-Do-List"].append(data.item)
    return {
        "status" : "success",
        "updated_list" : userInfo.info[data.id]["To-Do-List"]
    }

@app.post("/Register")
async def register(data : UserAuth):
    if data.userId in userInfo.info:
        raise HTTPException(status_code = status.HTTP_400_BAD_REQUEST)
    taken_usernames = userInfo.taken_user
    
    if data.username in taken_usernames:
        raise HTTPException(status_code = status.HTTP_400_BAD_REQUEST)
    userInfo.taken_user.add(data.username)
    userInfo.info[data.userId] = {
        "Username" : data.username,
        "Password" : data.password,
        "To-Do-List" : []
    }
    return {"status" : "success"}


@app.put("/DeleteList")
async def deleteList(data : UpdateList):
    if data.id in userInfo.info:
        updatedList = data.todo_list
        userInfo.deleted_List.append(data.deleted_list)
        userInfo.info[data.id]["To-Do-List"] = updatedList
        todoList = userInfo.info[data.id]["To-Do-List"]
        return {
            "status" : "succes",
            "deleted-list" : userInfo.deleted_List,
            "updated-list" : todoList
        }
    raise HTTPException(status_code = status.HTTP_401_UNAUTHORIZED)