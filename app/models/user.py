from app.config import Base

import enum

from fastapi_users_db_sqlalchemy import SQLAlchemyBaseUserTableUUID

from sqlalchemy import Enum, ForeignKey
from sqlalchemy.orm import relationship

from typing import Literal, get_args

from sqlalchemy.orm import Mapped, mapped_column


class Role(str, enum.Enum):
    admin = "admin"
    manager = "manager"
    user = "user"


class TeamRole(str, enum.Enum):
    manager = "manager"
    employee = "employee"


RoleType = Literal["admin", "manager", "user"]

TeamRoleType = Literal["manager", "employee"]


class UserModel(SQLAlchemyBaseUserTableUUID, Base):
    __tablename__ = "users"

    role: Mapped[RoleType] = mapped_column(
        Enum(*get_args(RoleType), name="role_enum", metadata=Base.metadata),
        default="user",
    )
    team_role: Mapped[TeamRoleType] = mapped_column(
        Enum(*get_args(TeamRoleType), name="team_role_enum", native_enum=False),
        default=TeamRole.employee,
        nullable=True,
    )

    team_id: Mapped[int] = mapped_column(ForeignKey("teams.id"), nullable=True)

    team: Mapped["TeamModel"] = relationship("TeamModel", back_populates="users")

    def __str__(self) -> str:
        return f"{self.email}"
