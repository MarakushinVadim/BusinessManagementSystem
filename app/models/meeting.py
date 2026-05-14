from app.config import Base

from datetime import datetime

from fastapi_users_db_sqlalchemy.generics import GUID

from sqlalchemy import DateTime, Table, Column, ForeignKey, Integer, String, Boolean
from sqlalchemy.orm import Mapped, mapped_column, relationship

users_meetings = Table(
    "users_meetings",
    Base.metadata,
    Column("user_id", GUID(), ForeignKey("users.id"), primary_key=True, index=True),
    Column(
        "meeting_id", Integer, ForeignKey("meetings.id"), primary_key=True, index=True
    ),
)


class MeetingModel(Base):
    __tablename__ = "meetings"

    id: Mapped[int] = mapped_column(primary_key=True)
    title: Mapped[str] = mapped_column(String(50), nullable=True)
    description: Mapped[str] = mapped_column(String(500), nullable=True)
    date: Mapped[datetime] = mapped_column(DateTime, nullable=False)
    participants: Mapped[list["UserModel"]] = relationship(
        "UserModel",
        secondary=users_meetings,
        back_populates="meetings",
        cascade="save-update, merge",
        uselist=True,
    )
    canceled: Mapped[bool] = mapped_column(Boolean, nullable=True)
