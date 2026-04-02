from datetime import datetime
import uuid

from pydantic import BaseModel, Field

from typing import Optional


class TaskCreate(BaseModel):
    title: str = Field(description="Название задачи")
    description: str = Field(description="Описание задачи")
    deadline: datetime = Field(description="Выполнить до:")
    status: str = Field(description="Статус задачи")


class TaskRead(TaskCreate):
    id: int = Field(description="ID задачи")
    author_id: uuid.UUID = Field(description="ID автора")
    performer_id: Optional[uuid.UUID] = Field(description="ID исполнителя")


class TaskUpdate(TaskCreate):
    performer_id: uuid.UUID = Field(description="ID исполнителя")
