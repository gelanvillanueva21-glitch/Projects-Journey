from pydantic import BaseModel, EmailStr, Field, ConfigDict, model_validator
from typing import Annotated
from datetime import datetime



class UserBase(BaseModel):
    name : str
    email : EmailStr



class CreateUser(UserBase):
    password : Annotated[str, Field(min_length = 8, max_length = 50)]



class UserResponse(BaseModel):
    name : str
    is_active : Annotated[bool, Field(default = True)]
    available_balance : int
    
    model_config = ConfigDict(from_attributes = True)




class LoanMoney(BaseModel):
    loan_value : Annotated[int, Field(ge=1000, le=10000)]
    monthly_due_date : datetime | None = None
    due_date : datetime | None = None
    
    # The purpose of this is to make the user choose whatever
    # payment they want
    @model_validator(mode="after")
    def validate_clean_date(self):
        
        has_due_date = self.due_date is not None
        has_monthly_due_date = self.monthly_due_date is not None
        
        # if both of the date payment is none
        # then we raise an error
        if not has_due_date and not has_monthly_due_date:
            raise ValueError("You must provide either 'due_date' or 'monthly_due_date'.")
        
        # if both has value then we raise and error too
        if has_due_date and has_monthly_due_date:
            raise ValueError("You cannot provide both 'due_date' and 'monthly_due_date'. Pick only one.")
        
        # if due_date has value and the tzinfo is none then
        # this is the payment date method the user want
        if has_due_date and self.due_date.tzinfo is not None:
            self.due_date = self.due_date.replace(tzinfo=None)
        
        # if monthly_due_date has value and the tzinfo has value aswell
        # then the user pick monthly due date
        if has_monthly_due_date and self.monthly_due_date.tzinfo is not None:
            self.monthly_due_date = self.monthly_due_date.replace(tzinfo=None)
        return self



class LoanRespons(LoanMoney):
    model_config = ConfigDict(from_attributes = True)



class LoanPay(BaseModel):
    paid_amount : int
    
    model_config = ConfigDict(from_attributes = True)



class Token(BaseModel):
    access_token : str
    token_type : str





