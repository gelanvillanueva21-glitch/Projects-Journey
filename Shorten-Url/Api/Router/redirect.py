from datetime import datetime, timezone
from fastapi import APIRouter, Depends, HTTPException, status, BackgroundTasks, Request
from fastapi.responses import RedirectResponse
from sqlalchemy.ext.asyncio import AsyncSession
from typing import Annotated
from database import get_database
from crud import record_click, get_url_db



router = APIRouter()



@router.get("/{short_code}")
async def redirect(
    database : Annotated[AsyncSession, Depends(get_database)],
    short_code : str,
    request : Request,
    background_task : BackgroundTasks):

        url = await get_url_db(database, short_code)
        if not url or (url.expires_at and url.expires_at < datetime.now(timezone.utc)):
            raise HTTPException(
                status_code = status.HTTP_404_NOT_FOUND,
                detail = "Linked not found or expired"
            )
        ip_address = request.client.host if request.client else None
        background_task.add_task(record_click, database, url.id, ip_address)
        return RedirectResponse(
            url.original_url,
            status_code = status.HTTP_307_TEMPORARY_REDIRECT
        )



