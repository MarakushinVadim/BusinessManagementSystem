from datetime import datetime

from app.config import Base

from sqlalchemy import String, DateTime, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from uuid import UUID

from fastapi_users_db_sqlalchemy.generics import GUID


class CommentModel(Base):
    __tablename__ = "comments"

    id: Mapped[int] = mapped_column(primary_key=True)
    text: Mapped[str] = mapped_column(String, nullable=False)
    username: Mapped[str] = mapped_column(String, nullable=True)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.now)

    task_id: Mapped[int] = mapped_column(ForeignKey("tasks.id"), nullable=False)
    user_id: Mapped[UUID] = mapped_column(
        GUID(), ForeignKey("users.id"), nullable=False
    )

    task: Mapped["TaskModel"] = relationship("TaskModel", back_populates="comments")

    users: Mapped[list["UserModel"]] = relationship(
        "UserModel", back_populates="comments"
    )
