from datetime import datetime
from typing import Optional

from fastapi import APIRouter, Depends, status

import app.schemas.calendar
from app.auth.auth import fastapi_user_model
from app.models import UserModel, MeetingModel
from app.services import get_events
from app.database import get_async_session
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from sqlalchemy.orm import selectinload

router = APIRouter(
    prefix="/calendar",
    tags=["calendar"],
)

current_active_user = fastapi_user_model.current_user()


@router.get("/", response_model=app.schemas.calendar.CalendarSchema)
async def get_calendar(
    user: UserModel = Depends(current_active_user),
    session: AsyncSession = Depends(get_async_session),
):
    await session.refresh(user, attribute_names=["meetings", "tasks"])

    response = await get_events(user, None, None)

    return response


@router.get("/per_day", response_model=app.schemas.calendar.CalendarSchema)
async def get_calendar_per_day(
    day: Optional[datetime] = None,
    user: UserModel = Depends(current_active_user),
    session: AsyncSession = Depends(get_async_session),
):
    if not day:
        day = datetime.today()

    await session.refresh(user, attribute_names=["meetings", "tasks"])

    response = await get_events(user, day, None)

    return response


@router.get("/per_month", response_model=app.schemas.calendar.CalendarSchema)
async def get_calendar_per_month(
    month: Optional[datetime] = None,
    user: UserModel = Depends(current_active_user),
    session: AsyncSession = Depends(get_async_session),
):
    if not month:
        month = datetime.today()

    month = month.replace(day=1, hour=0, minute=0, second=0, microsecond=0)

    print("route month", month)

    await session.refresh(user, attribute_names=["meetings", "tasks"])

    response = await get_events(user, None, month)

    return response
