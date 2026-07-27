from pydantic import BaseModel, EmailStr, Field, ConfigDict
from typing import Annotated
from datetime import datetime



class UserBase(BaseModel):
    name : str
    email : EmailStr



class CreateUser(UserBase):
    password : Annotated[str, Field(min_length = 8, max_length = 50)]



class UserResponse(BaseModel):
    email : EmailStr
    is_active : Annotated[bool, Field(default = True)]
    
    model_config = ConfigDict(from_attributes = True)




class LoanMoney(BaseModel):
    loan_value : int
    anual_interest_rate : int
    monthly_due_date : datetime | None = None
    due_date : datetime | None = None



class LoanRespons(LoanMoney):
    model_config = ConfigDict(from_attributes = True)



class LoanPay(BaseModel):
    paid_amount : int
    
    model_config = ConfigDict(from_attributes = True)



class Token(BaseModel):
    access_token : str
    token_type : str





