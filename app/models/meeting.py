from app.config import Base

from datetime import datetime

from sqlalchemy import DateTime
from sqlalchemy.orm import Mapped, mapped_column, relationship

class MeetingModel(Base):
    __tablename__ = 'meetings'

    id: Mapped[int] = mapped_column(primary_key=True)
    date: Mapped[datetime] = mapped_column(DateTime, nullable=False)
    participants: Mapped[list["UserModel"]] = relationship(
        "UserModel",
        back_populates="meetings",
        cascade="save-update, merge",
        uselist=True
    )