from app.database import Base
from app.models.task import TaskModel

from fastapi_users.db import SQLAlchemyBaseUserTableUUID

from enum import Enum

from typing import Literal, get_args

from sqlalchemy import String, Boolean
from sqlalchemy.orm import Mapped, mapped_column, relationship


class Role(str, Enum):
    admin = "admin"
    manager = "manager"
    user = "user"


RoleType = Literal["admin", "manager", "user"]


class UserModel(SQLAlchemyBaseUserTableUUID, Base):
    __tablename__ = "users"

    role: Mapped[RoleType] = mapped_column(
        Enum(*get_args(RoleType), name="role_enum", metadata=Base.metadata),
        default="user",
    )

    tasks: Mapped[list["TaskModel"]] = relationship(
        back_populates="author",
        cascade="all, delete-orphan",
    )
