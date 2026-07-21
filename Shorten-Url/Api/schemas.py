from datetime import datetime
from pydantic import BaseModel, EmailStr, Field, ConfigDict, computed_field
from typing import Annotated



class CreateUser(BaseModel):
    email : EmailStr
    password : Annotated[str, Field(
        min_length = 8,
        max_length = 50)]


class UserResponse(BaseModel):
    id : int
    email : EmailStr
    is_active : Annotated[bool, Field(default = True)]
    
    model_config = ConfigDict(from_attributes = True)


class TokenResponse(BaseModel):
    access_token : str
    token_type : str
    
    model_config = ConfigDict(from_attributes = True)



class UrlCreate(BaseModel):
    original_url : Annotated[str, Field(max_length = 2028)]
    custom_code: Annotated[str | None, Field(max_length=12, default=None)]
    expires_at: Annotated[datetime | None, Field(default=None)]


class UrlResponse(BaseModel):
    id : int
    original_url : Annotated[str, Field(max_length = 2028)]
    short_code : Annotated[str, Field(max_length = 12)]
    created_at : datetime
    expires_at : datetime | None
    
    model_config = ConfigDict(from_attributes = True)
    
    @computed_field
    @property
    def short_url(self) -> str:
        return f"https://urlshortened.com/{self.short_code}"


class ClickResponse(BaseModel):
    id : int
    url_id : int
    clicked_at : datetime
    ip_address : Annotated[str | None, Field(max_length = 40)]

