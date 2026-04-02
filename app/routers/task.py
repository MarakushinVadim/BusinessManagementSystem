from fastapi import APIRouter, Depends, status
from app import schemas
from app.auth.auth import fastapi_user_model
from sqlalchemy.ext.asyncio import AsyncSession
from app.database import get_async_session
from app.models import UserModel, TaskModel

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
    await session.commit()
    await session.refresh(task_db)

    return task_db
