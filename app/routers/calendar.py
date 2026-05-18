from datetime import datetime
from typing import Optional

from fastapi import APIRouter, Depends, status, Request

import app.schemas.calendar
from app.auth.auth import current_active_user
from app.config import templates
from app.models import UserModel
from app.services import get_events
from app.database import get_async_session
from sqlalchemy.ext.asyncio import AsyncSession

router = APIRouter(
    prefix="/calendar",
    tags=["calendar"],
)


@router.get(
    "/",
    response_model=app.schemas.calendar.CalendarSchema,
    status_code=status.HTTP_200_OK,
)
async def get_calendar(
    request: Request,
    user: UserModel = Depends(current_active_user),
    session: AsyncSession = Depends(get_async_session),
):
    await session.refresh(user, attribute_names=["meetings", "tasks"])

    response = await get_events(user, None, None)

    accept_header = request.headers.get("accept", "")
    if "text/html" in accept_header:
        return templates.TemplateResponse(
            request=request,
            name="calendar.html",
            context={"events_data": response, "user": user},
        )

    return response


@router.get(
    "/per_day",
    response_model=app.schemas.calendar.CalendarSchema,
    status_code=status.HTTP_200_OK,
)
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


@router.get(
    "/per_month",
    response_model=app.schemas.calendar.CalendarSchema,
    status_code=status.HTTP_200_OK,
)
async def get_calendar_per_month(
    month: Optional[datetime] = None,
    user: UserModel = Depends(current_active_user),
    session: AsyncSession = Depends(get_async_session),
):
    if not month:
        month = datetime.today()

    month = month.replace(day=1, hour=0, minute=0, second=0, microsecond=0)

    await session.refresh(user, attribute_names=["meetings", "tasks"])

    response = await get_events(user, None, month)

    return response
