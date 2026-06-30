from fastapi import FastAPI, HTTPException, status
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field
from typing import Annotated

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
    username : Annotated[str, Field(
        min_length = 3, 
        max_length = 50, 
        pattern = r"^[a-zA-Z0-9_-]+$",
        description = "3-20 characters. Only letters, numbers, underscores, or hyphens."
        )]
    password : Annotated[str, Field(
        min_length = 8,
        max_length = 20,
        pattern=r"^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[@$!%*?&])[A-Za-z\d@$!%*?&]{8,}$",
        description="At least 8 characters long, with 1 uppercase, 1 lowercase, 1 number, and 1 special symbol."
    )]





