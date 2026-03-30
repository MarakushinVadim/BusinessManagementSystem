from app.config import Base

from app.models.user import UserModel

from datetime import datetime

from typing import Literal, get_args

from sqlalchemy import Enum

from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import ForeignKey, String, DateTime, Integer


class TaskStatus(str, Enum):
    open = "open"
    in_work = "in_work"
    done = "done"


StatusType = Literal["open", "in_work", "done"]


class TaskModel(Base):
    __tablename__ = "tasks"

    id: Mapped[int] = mapped_column(primary_key=True)
    title: Mapped[str] = mapped_column(String(50), nullable=False)
    description: Mapped[str] = mapped_column(String, nullable=True)
    deadline: Mapped[datetime] = mapped_column(DateTime, nullable=False)
    status: Mapped[StatusType] = mapped_column(
        Enum(*get_args(StatusType), name="status_enum", metadata=Base.metadata),
        default="open",
    )

    performer_id: Mapped[int] = mapped_column(
        Integer, ForeignKey("users.id"), nullable=True
    )
    author_id: Mapped[int] = mapped_column(
        Integer, ForeignKey("users.id"), nullable=False
    )
