from uuid import UUID

from fastapi_users_db_sqlalchemy.generics import GUID

from app.config import Base

from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship


class TeamModel(Base):
    __tablename__ = "teams"

    id: Mapped[int] = mapped_column(primary_key=True)

    admin_id: Mapped[UUID] = mapped_column(
        GUID(),
        ForeignKey("users.id", use_alter=True, name="fk_team_admin_id"),
        nullable=True,
    )

    users: Mapped[list["UserModel"]] = relationship(
        "UserModel",
        back_populates="team",
        cascade="save-update, merge",
        foreign_keys="[UserModel.team_id]",
    )
