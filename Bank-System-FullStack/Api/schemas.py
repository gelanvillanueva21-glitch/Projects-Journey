from pydantic import BaseModel, EmailStr, Field, ConfigDict
from typing import Annotated
from datetime import datetime



class UserBase(BaseModel):
    email : EmailStr



class CreateUser(UserBase):
    password : Annotated[str, Field(min_length = 8, max_length = 50)]



class UserResponse(BaseModel):
    id : int
    email : EmailStr
    is_active : Annotated[bool, Field(default = True)]
    
    model_config = ConfigDict(from_attributes = True)




class Laon(BaseModel):
    deptor_id : int
    lender_id : int
    loan_value : int
    anual_interest_rate : int
    monthly_due_date : datetime | None
    due_date : datetime | None



class LoanRespone(BaseModel):
    loan_value : int
    anual_interest_rate : int
    monthly_due_date : datetime | None
    due_date : datetime | None
    
    model_config = ConfigDict(from_attributes = True)



class Withdraw(BaseModel):
    id : int
    withdraw_amount : int



class Deposit(BaseModel):
    id : int
    deposit_amount : int





