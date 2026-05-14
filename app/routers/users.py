import uuid

from fastapi import APIRouter, Depends, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, update
from sqlalchemy.orm import selectinload

from app.database import get_async_session
from app.models import UserModel
from app.auth.auth import fastapi_user_model
# from app.schemas.task import RatingList
from app.services import check_admin, check_user_exists
from app.schemas import UserUpdate, UserRead, RatingList

router = APIRouter(prefix="/auth/users", tags=["users"])

current_active_user = fastapi_user_model.current_user()

@router.delete("/admin_delete/{user_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_user(
        user_id: uuid.UUID,
        session: AsyncSession = Depends(get_async_session),
        user: UserModel = Depends(current_active_user)
):

    await check_admin(user)
    result = await session.execute(
        select(UserModel)
        .where(UserModel.id == user_id)
    )


    user_for_delete = result.scalar_one_or_none()

    await check_user_exists(user_for_delete)

    await session.delete(user_for_delete)
    await session.commit()

    return None


@router.patch("/admin_patch/user_id", response_model=UserRead, status_code=status.HTTP_200_OK)
async def admin_update_user(
        user_id: uuid.UUID,
        user_data: UserUpdate,
        session: AsyncSession = Depends(get_async_session),
        user: UserModel = Depends(current_active_user)
):

    await check_admin(user)

    result = await session.execute(
        select(UserModel)
        .where(UserModel.id == user_id)
    )

    updated_user = result.scalar_one_or_none()

    await check_user_exists(updated_user)

    data_for_update = {}

    for data in user_data:
        if data[1]:
            data_for_update[data[0]] = data[1]

    await session.execute(
        update(UserModel)
        .where(UserModel.id == user_id)
        .values(**data_for_update)
    )



    await session.commit()

    updated_db_user = (await session.scalars(
        select(UserModel)
        .where(UserModel.id == user_id)
    )).first()

    return updated_db_user

@router.get("/me/my_rates", response_model=RatingList)
async def get_my_rates(
        user: UserModel = Depends(current_active_user),
        session: AsyncSession = Depends(get_async_session),
):

    await session.refresh(user, attribute_names=['ratings'])

    return {"ratings": user.ratings}

