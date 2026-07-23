from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from typing import Annotated
from crud import create_url, get_url_db, get_urls_by_user
from schemas import UrlResponse, UrlCreate
from models import User
from database import get_database
from Router.authentication import get_current_user



router = APIRouter(prefix = "/urls", tags = ["urls"])


@router.post(
    "/create", 
    status_code = status.HTTP_201_CREATED, 
    response_model = UrlResponse)
async def add_url(
    database : Annotated[AsyncSession, Depends(get_database)],
    current_user : Annotated[User, Depends(get_current_user)],
    url_data : UrlCreate):
        try:
            
            result = await create_url(database, url_data, current_user.id)
            return result
        except ValueError as e:
            raise HTTPException(
                status_code = status.HTTP_400_BAD_REQUEST,
                detail = str(e)
            )



@router.get("/myurl")
async def get_url(
    database : Annotated[AsyncSession, Depends(get_database)],
    current_user : Annotated[User, Depends(get_current_user)]
) -> list[UrlResponse]:
        try:
            
            result = await get_urls_by_user(database, current_user.id)
            return result
        except ValueError as e:
            raise HTTPException(
                status_code = status.HTTP_400_BAD_REQUEST,
                detail = str(e)
            )



