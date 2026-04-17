import enum

from uuid import UUID

from fastapi_users_db_sqlalchemy.generics import GUID

from app.config import Base

from sqlalchemy import Enum, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from typing import Literal, get_args


class TeamRole(str, enum.Enum):
    manager = "manager"
    employee = "employee"


RoleType = Literal["manager", "employee"]


class TeamModel(Base):
    __tablename__ = "teams"

    id: Mapped[int] = mapped_column(primary_key=True)
    team_role: Mapped[RoleType] = mapped_column(
        Enum(*get_args(TeamRole), name="team_role_enum", native_enum=False),
        default=TeamRole.employee,
        nullable=False,
    )
    admin_id: Mapped[UUID] = mapped_column(
        GUID(), ForeignKey("users.id"), nullable=True
    )

    users: Mapped[list["UserModel"]] = relationship(
        "User", back_populates="team", cascade="save-update, merge"
    )
