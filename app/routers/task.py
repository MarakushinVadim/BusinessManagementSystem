from fastapi import APIRouter, Depends, status, HTTPException, Query

from app import schemas
from app.auth.auth import fastapi_user_model
from sqlalchemy import select, update
from sqlalchemy.orm import selectinload
from sqlalchemy.ext.asyncio import AsyncSession
from app.database import get_async_session
from app.models import UserModel, TaskModel, RatingModel, CommentModel
from app.services import check_current_task_exist, check_author, check_task_done

from loguru import logger

router = APIRouter(
    prefix="/tasks",
    tags=["tasks"],
)

current_active_user = fastapi_user_model.current_user()


@router.post("/", response_model=schemas.TaskRead, status_code=status.HTTP_201_CREATED)
async def create_task(
    task: schemas.TaskCreate,
    user: UserModel = Depends(current_active_user),
    session: AsyncSession = Depends(get_async_session),
):

    task_data = task.model_dump()

    if task_data.get("deadline") and task_data["deadline"].tzinfo:
        task_data["deadline"] = task_data["deadline"].replace(tzinfo=None)

    task_db = TaskModel(**task_data, author_id=user.id)
    session.add(task_db)
    try:
        await session.commit()
        await session.refresh(task_db)
    except Exception as e:
        logger.error(e)
        await session.rollback()
        raise e

    return task_db


@router.get("/", response_model=list[schemas.TaskRead], status_code=status.HTTP_200_OK)
async def get_all_tasks(session: AsyncSession = Depends(get_async_session)):

    tasks = (
        await session.scalars(
            select(TaskModel)
            .order_by(TaskModel.deadline.desc())
            .options(selectinload(TaskModel.comments))
        )
    ).all()
    for task in tasks:
        # task_dict = None
        # if task.comments:
        #     task_dict = schemas.CommentOut.model_validate(task.comments).model_dump()
        # for comment in task.comments:
        #     print(comment)
        print(task.comments)


    if tasks:
        return tasks
    return []


@router.patch(
    "/{task_id}", response_model=schemas.TaskRead, status_code=status.HTTP_200_OK
)
async def assign_task_performer(
    task_id: int,
    performer_id: str = Query(description="Введите id исполнителя"),
    session: AsyncSession = Depends(get_async_session),
    current_user: UserModel = Depends(current_active_user),
):

    task = (
        await session.scalars(select(TaskModel).where(TaskModel.id == task_id))
    ).first()

    if not task:
        message = "Задача с таким id не найдена"
        logger.error(message)
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=message)

    if not task.author_id == current_user.id:
        # print("task author = " task)
        message = "Вносить изменения в задачу может только её автор!"
        logger.error(message)
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=message)

    performer = (
        await session.scalars(select(UserModel).where(UserModel.id == performer_id))
    ).first()

    if not performer:
        message = "Пользователь с таким e-mail не найден!"
        logger.error(message)
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=message)

    updated_task = (
        await session.execute(
            update(TaskModel)
            .where(TaskModel.id == task_id)
            .values(performer_id=performer.id, status="in_work")
            .returning(TaskModel)
        )
    ).scalar_one()
    try:
        await session.commit()
        await session.refresh(updated_task)
        return updated_task
    except Exception as e:
        logger.error(e)
        await session.rollback()
        raise e


@router.patch(
    "/update/{task_id}", response_model=schemas.TaskRead, status_code=status.HTTP_200_OK
)
async def update_task(
    task_id: int,
    task: schemas.TaskUpdate,
    session: AsyncSession = Depends(get_async_session),
    current_user: UserModel = Depends(current_active_user),
):

    current_task = (
        await session.scalars(select(TaskModel).where(TaskModel.id == task_id))
    ).first()

    if not current_task:
        message = "Задача с таким id не найдена"
        logger.error(message)
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=message)

    if not current_task.author_id != current_user.id:
        message = "Вносить изменения в задачу может только её автор!"
        logger.error(message)
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=message)

    values = {}

    if task.title:
        values["title"] = task.title
    if task.description:
        values["description"] = task.description
    if task.deadline:
        values["deadline"] = task.deadline.replace(tzinfo=None)
    if task.status:
        values["status"] = task.status
    if task.performer_id:
        values["performer_id"] = task.performer_id

    updated_task = (
        await session.execute(
            update(TaskModel)
            .where(TaskModel.id == task_id)
            .values(**values)
            .returning(TaskModel)
        )
    ).scalar_one()
    try:
        await session.commit()
        await session.refresh(updated_task)
        return updated_task
    except Exception as e:
        logger.error(e)
        await session.rollback()
        raise e


@router.get(
    "/{task_id}", response_model=schemas.TaskRead, status_code=status.HTTP_200_OK
)
async def detail_task(
    task_id: int,
    session: AsyncSession = Depends(get_async_session),
):
    current_task = (
        await session.scalars(select(TaskModel).where(TaskModel.id == task_id))
    ).first()

    if not current_task:
        message = "Задача с таким id не найдена"
        logger.error(message)
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=message)

    return current_task

@router.post('/{task_id}/rate/')
async def create_rating(
        task_id: int,
        rate: schemas.RatingCreate,
        session: AsyncSession = Depends(get_async_session),
        current_user: UserModel = Depends(current_active_user)
):

    current_task = (await session.scalars(select(TaskModel).where(TaskModel.id == task_id))).first()

    check_current_task_exist(current_task)

    await check_author(current_task, current_user)

    await check_task_done(current_task)

    rate_data = rate.model_dump()

    if not rate_data:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST)

    rate_db = RatingModel(
        **rate_data,
        task_id=task_id,
        performer_id=current_user.id
    )

    session.add(rate_db)

    await session.commit()
    await session.refresh(current_task)
