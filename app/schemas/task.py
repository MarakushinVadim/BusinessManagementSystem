from datetime import datetime
import uuid

from pydantic import BaseModel, Field

from typing import Optional, TYPE_CHECKING, Literal

if TYPE_CHECKING:
    from app.schemas.comment import CommentOut, CommentList
    from app.schemas.user import UserShort


class TaskCreate(BaseModel):
    title: str = Field(description="Название задачи")
    description: str = Field(description="Описание задачи")
    deadline: datetime = Field(description="Выполнить до:")
    status: Optional[str] = None


class TaskRead(TaskCreate):
    id: int = Field(description="ID задачи")
    author: "UserShort"
    performer: Optional["UserShort"] = []
    author_id: uuid.UUID = Field(description="ID автора")
    performer_id: Optional[uuid.UUID] = Field(description="ID исполнителя")
    comments: Optional[list["CommentOut"]] = []
    rating: Optional["RatingCreate"] = []

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


class TaskShort(BaseModel):
    id: int
    title: Optional[str] = None
    description: Optional[str] = None
    deadline: datetime
    rating: Optional[int] = None


TaskTuple = tuple[Literal["tasks"], list[TaskShort]]


class RatingCreate(BaseModel):
    rate: int = Field(ge=1, le=5)


class Rating(BaseModel):
    rate: int

    class Config:
        from_attributes = True


class RatingList(BaseModel):
    ratings: list["Rating"]

    class Config:
        from_attributes = True


from app.schemas.comment import CommentOut, CommentList
from app.schemas.user import UserShort

TaskRead.model_rebuild()
