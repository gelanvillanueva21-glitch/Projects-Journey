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




class LaonMoney(BaseModel):
    loan_value : int
    anual_interest_rate : int
    monthly_due_date : datetime | None = None
    due_date : datetime | None = None



class LoanRespone(LaonMoney):
    model_config = ConfigDict(from_attributes = True)



class LoanPay(BaseModel):
    paid_amount : int
    
    model_config = ConfigDict(from_attributes = True)


class WithdrawMoney(BaseModel):
    id : int
    amount : int



class DepositMoney(BaseModel):
    id : int
    amount : int





