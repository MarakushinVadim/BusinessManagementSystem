from fastapi import APIRouter, status, Depends

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, desc

from loguru import logger

from app import schemas
from app.database import get_async_session
from app.models import TaskModel, UserModel, CommentModel
from app.routers.task import current_active_user
from app.services import check_current_task_exist

router = APIRouter(prefix="/comments", tags=["comments"])


@router.get(
    "/{task_id}", response_model=schemas.CommentList, status_code=status.HTTP_200_OK
)
async def get_comments(
    task_id: int, session: AsyncSession = Depends(get_async_session)
):
    current_task = (
        await session.scalars(select(TaskModel).where(TaskModel.id == task_id))
    ).first()

    check_current_task_exist(current_task)

    comments = (
        await session.scalars(
            select(CommentModel)
            .where(CommentModel.task_id == current_task.id)
            .order_by(desc(CommentModel.created_at))
        )
    ).all()
    if not comments:
        comments = []

    return {"comments": comments}


@router.post(
    "/{task_id}", response_model=schemas.CommentOut, status_code=status.HTTP_201_CREATED
)
async def create_comment(
    task_id: int,
    comment: schemas.CommentCreate,
    session: AsyncSession = Depends(get_async_session),
    current_user: UserModel = Depends(current_active_user),
):
    current_task = (
        await session.scalars(select(TaskModel).where(TaskModel.id == task_id))
    ).first()

    check_current_task_exist(current_task)

    comment_data = comment.model_dump()

    comment_db = CommentModel(
        **comment_data,
        task_id=current_task.id,
        user_id=current_user.id,
        username=current_user.email
    )

    session.add(comment_db)
    try:
        await session.commit()
        await session.refresh(comment_db)
    except Exception as e:
        logger.error(e)
        await session.rollback()
        raise e

    return comment_db
