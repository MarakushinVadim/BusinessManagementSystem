from app.database import Base
from app.models.task import Task

from enum import Enum

from typing import Literal, get_args

from sqlalchemy import String, Boolean
from sqlalchemy.orm import Mapped, mapped_column, relationship


class Role(str, Enum):
    admin = "admin"
    manager = "manager"
    user = "user"


RoleType = Literal["admin", "manager", "user"]


class UserModel(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(primary_key=True)
    email: Mapped[str] = mapped_column(String, unique=True, index=True, nullable=False)
    hashed_password: Mapped[str] = mapped_column(String, nullable=False)

    is_superuser: Mapped[bool] = mapped_column(Boolean, default=False)
    role: Mapped[RoleType] = mapped_column(
        Enum(*get_args(RoleType), name="role_enum", metadata=Base.metadata),
        default="user",
    )

    tasks: Mapped[list["Task"]] = relationship(
        back_populates="author",
        cascade="all, delete-orphan",
    )
