from fastapi import FastAPI, HTTPException, status, Depends
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field, field_validator
from typing import Annotated
from database import engine
from sqlalchemy.orm import Session
import model
import re

app = FastAPI()
model.Base.metadata.create_all(bind=engine)


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
    deleted_list : str
    id : int

class AddItemList(BaseModel):
    item : Annotated[str, Field(max_length = 35)]
    id : int


class CheckedList(BaseModel):
    checked_list : list[str] = [],
    id : int


@app.post("/Login")
async def logIn(
    user : UserAuth, 
    db : Annotated[Session, Depends(model.get_db)]):
    
    result = db.query(model.UserAuthInfo).filter(
        model.UserAuthInfo.id == user.userId,
        model.UserAuthInfo.username == user.username,
        model.UserAuthInfo.password == user.password
        ).first()
    if not result:
        raise HTTPException(
            status_code = status.HTTP_404_NOT_FOUND,
            detail = "Id or Username or Password Not Found"
        )
        
    todolist = [[todo.title, todo.is_complete] for todo in result.todolist]
    return {
        "status" : "success",
        "Todo-List" : todolist
    }


@app.post("/AddItem")
async def addItem(
    data : AddItemList, 
    db : Annotated[Session, Depends(model.get_db)]):
    
    result = db.query(model.UserAuthInfo).filter(model.UserAuthInfo.id == data.id).first()
    if not result:
        raise HTTPException(
            status_code = status.HTTP_401_UNAUTHORIZED,
            detail = "Id Not Found"
        )
    items = [todo.title for todo in result.todolist]
    
    if data.item in items:
        raise HTTPException(
            status_code = status.HTTP_400_BAD_REQUEST,
            detail = "Item Already Exist"
        )
        
    newItemList = model.Todo(
        title = data.item,
        user_id = data.id
    )
    db.add(newItemList)
    db.commit()
    db.refresh(newItemList)
    
    return {
        "status" : "success",
        "updated_list" : [todo.title for todo in result.todolist]
    }

@app.post("/Register")
async def register(
    data : UserAuth, 
    db : Annotated[Session, Depends(model.get_db)]):
    
    new_user = model.UserAuthInfo(
        id = data.userId,
        username = data.username,
        password = data.password
    )
    try:
        
        db.add(new_user)
        db.commit()
        return {"status" : "success"}
    except:
        
        raise HTTPException(
            status_code = status.HTTP_400_BAD_REQUEST,
            detail = "Username or Id might already created by someone"
        )


@app.delete("/DeleteList")
async def deleteList(
    data : UpdateList, 
    db : Annotated[Session, Depends(model.get_db)]):
    
    result = db.query(model.UserAuthInfo).filter(model.UserAuthInfo.id == data.id).first()
    if not result:
        raise HTTPException(
            status_code = status.HTTP_403_FORBIDDEN,
            detail = "ID Does Not Exist"
        )
    
    try:
        
        target_item = db.query(model.Todo).filter(
            model.Todo.title == data.deleted_list,
            model.Todo.user_id == data.id
        ).first()
        
        if not target_item:
            raise KeyError("Item Not Found")
        
        db.delete(target_item)
        db.commit()
        
        updatedItem = [ [todo.title, todo.is_complete] for todo in result.todolist ]
        
        return {
            "status" : "success",
            "updated-item" : updatedItem
        }
    except KeyError:
        
        raise HTTPException(
            status_code = status.HTTP_404_NOT_FOUND,
            detail = "Item does not exist in your list"
        )
    except Exception as e:
        db.rollback()
        raise HTTPException(
            status_code = status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail = "An Internal database error occured"
        )


@app.put("/UpdateChecked")
async def updateCheckList(
    data : CheckedList, 
    db : Annotated[Session, Depends(model.get_db)]):
    
    result = db.query(model.UserAuthInfo).filter(model.UserAuthInfo.id == data.id).first()
    if not result:
        raise HTTPException(
            status_code = status.HTTP_401_UNAUTHORIZED,
            detail = "Id Does Not Exist"
        )
    
    try:

        todo_item = db.query(model.Todo).filter(model.Todo.user_id == data.id).all()
            
        if not todo_item:
            raise KeyError("Item Not Found")
            
        for todo in todo_item:
            if todo.title in data.checked_list:
                todo.is_complete = True
            else:
                todo.is_complete = False
        
        db.commit()
        todo_update = [ [todo.title, todo.is_complete] for todo in result.todolist ]
        return {
            "status" : "success",
            "update-list" : todo_update
        }
    except KeyError:
        
        raise HTTPException(
            status_code = status.HTTP_404_NOT_FOUND,
            detail = "Item Or Id Not Found"
        )
    except Exception as e:
        db.rollback()
        raise HTTPException(
            status_code = status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail = "An internal database error occurred"
        )



@app.get("/GetItems")
async def getListItems(
    id : Annotated[int, Field(ge = 99, le = 100000000000)], 
    db : Annotated[Session, Depends(model.get_db)]):
    
    result = db.query(model.UserAuthInfo).filter(model.UserAuthInfo.id == id).first()
    if not result:
        raise HTTPException(
            status_code = status.HTTP_404_NOT_FOUND,
            detail = "Id Not Found"
        )
    
    todolist = [[todo.title, todo.is_complete] for todo in result.todolist]
    return {
        "status" : "succes",
        "Todo-List" : todolist
    }


