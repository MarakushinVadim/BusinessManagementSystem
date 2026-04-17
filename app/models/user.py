from app.config import Base

from fastapi_users_db_sqlalchemy import SQLAlchemyBaseUserTableUUID

from sqlalchemy import Enum, ForeignKey
from sqlalchemy.orm import relationship

from typing import Literal, get_args

from sqlalchemy.orm import Mapped, mapped_column


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
    team_id: Mapped[int] = mapped_column(ForeignKey("teams.id"), nullable=True)

    team: Mapped["TeamModel"] = relationship("TeamModel", back_populates="users")

    def __str__(self) -> str:
        return f"{self.email}"
