import enum

from app.config import Base

from uuid import UUID

from fastapi_users_db_sqlalchemy.generics import GUID

from datetime import datetime

from typing import Literal, get_args

from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import ForeignKey, String, DateTime, Enum


class TaskStatus(str, enum.Enum):
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
        Enum(*get_args(StatusType), name="status_enum", native_enum=False),
        default=TaskStatus.open,
        nullable=False,
    )
    comments: Mapped["CommentModel"] = relationship(
        "CommentModel",
        back_populates="task",
        lazy="selectin",
        cascade="all, delete-orphan",
    )

    rating: Mapped["RatingModel"] = relationship(
        "RatingModel",
        back_populates="task",
        lazy="selectin",
        cascade="all, delete-orphan",
        uselist=False
    )

    performer_id: Mapped[UUID] = mapped_column(
        GUID(), ForeignKey("users.id"), nullable=True
    )
    author_id: Mapped[UUID] = mapped_column(
        GUID(), ForeignKey("users.id"), nullable=True
    )

class RatingModel(Base):
    __tablename__ = "ratings"

    id: Mapped[int] = mapped_column(primary_key=True)
    rate: Mapped[int] = mapped_column(nullable=True)

    task_id: Mapped[int] = mapped_column(ForeignKey("tasks.id"), nullable=False, unique=True)
    performer_id: Mapped[UUID] = mapped_column(GUID(), ForeignKey("users.id"))

    task: Mapped[TaskModel] = relationship(
        "TaskModel",
        back_populates="rating",
        uselist=False
    )
    user: Mapped[UUID] = relationship(
        "UserModel",
        back_populates="rating",
    )

