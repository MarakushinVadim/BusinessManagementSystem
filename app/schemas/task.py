from datetime import datetime
import uuid

from pydantic import BaseModel, Field, EmailStr

from typing import Optional, TYPE_CHECKING

if TYPE_CHECKING:
    from app.schemas.comment import CommentOut


class TaskCreate(BaseModel):
    title: str = Field(description="Название задачи")
    description: str = Field(description="Описание задачи")
    deadline: datetime = Field(description="Выполнить до:")
    status: str = Field(description="Статус задачи")


class TaskRead(TaskCreate):
    id: int = Field(description="ID задачи")
    author_id: uuid.UUID = Field(description="ID автора")
    performer_id: Optional[uuid.UUID] = Field(description="ID исполнителя")
    comments: Optional[list["CommentOut"]] = []

    class Config:
        from_attributes = True


class TaskUpdate(BaseModel):
    title: Optional[str] = Field(default=None, description="Название задачи")
    description: Optional[str] = Field(default=None, description="Описание задачи")
    deadline: Optional[datetime] = Field(
        default=None, description="Выполнить до: в формате '2026-04-03T00:00:00'"
    )
    status: Optional[str] = Field(default=None, description="Статус задачи")
    performer_id: Optional[uuid.UUID] = Field(
        default=None, description="ID исполнителя"
    )

class RatingCreate(BaseModel):
    rating: int = Field(ge=1, le=5)


from app.schemas.comment import CommentOut

TaskRead.model_rebuild()
