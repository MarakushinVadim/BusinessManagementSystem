import uuid

from fastapi import APIRouter, Depends, status
from sqlalchemy import select
from sqlalchemy.orm import selectinload
from sqlalchemy.ext.asyncio import AsyncSession
from app.database import get_async_session
from app import schemas
from app.models import MeetingModel, UserModel

from app.services import check_free_datetime_for_meet

router = APIRouter(prefix="/meetings", tags=["Meet"])


@router.post("/", status_code=status.HTTP_201_CREATED)
async def create_meet(
    meet: schemas.MeetCreate, session: AsyncSession = Depends(get_async_session)
):
    meet_data = meet.model_dump()
    meet_data["date"] = meet_data["date"].replace(tzinfo=None)

    participants_list = (
        await session.scalars(
            select(UserModel)
            .where(UserModel.id.in_(meet_data["participants"]))
            .options(selectinload(UserModel.meetings))
        )
    ).all()
    meet_data["participants"] = participants_list

    for user in participants_list:
        for meeting in user.meetings:
            await check_free_datetime_for_meet(meet_data["date"], meeting, user)

    meet_db = MeetingModel(**meet_data)
    session.add(meet_db)
    await session.commit()
    return {
        "id": meet_db.id,
        "date": meet_db.date,
        "participants": [(user.id, user.email) for user in participants_list],
    }


@router.get("/", status_code=status.HTTP_200_OK)
async def get_meets_for_user(
    user_id: uuid.UUID, session: AsyncSession = Depends(get_async_session)
):
    user = (
        await session.scalars(
            select(UserModel)
            .where(UserModel.id == user_id)
            .options(selectinload(UserModel.meetings))
        )
    ).first()

    return {
        "meets": [
            (
                f"id встречи - {meet.id}",
                f"Дата встречи - {meet.date}",
                f"Название встречи - {meet.title}",
            )
            for meet in user.meetings
        ]
    }
