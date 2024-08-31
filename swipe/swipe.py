from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from engine_db import get_async_session
from .schemas import SwipeCreate
from .crud import handle_swipe

router = APIRouter()


@router.post("/swipe/")
async def swipe(swipe: SwipeCreate,
                session: AsyncSession = Depends(get_async_session)):
    return await handle_swipe(swipe, session)
