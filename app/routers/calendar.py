from fastapi import APIRouter, Depends, status

import app.schemas.calendar
from app.auth.auth import fastapi_user_model
from app.models import UserModel, MeetingModel
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

    date_list = list()
    meets_list = list()
    tasks_list = list()
    response = list()

    for meet in user.meetings:
        meets_list.append(meet)
        if meet.date.date() not in date_list:
            date_list.append(meet.date.date())

    for task in user.tasks:
        tasks_list.append(task)
        if task.deadline.date() not in date_list:
            date_list.append(task.deadline.date())

    for n, date in enumerate(date_list):
        response.append({str(date): [["tasks", []], ["meets", []]]})

        for meet in meets_list:
            if meet.date.date() == date:
                response[n][str(date)][1][1].append(meet)

        for task in tasks_list:
            if task.deadline.date() == date:
                response[n][str(date)][0][1].append(task)

    return response
