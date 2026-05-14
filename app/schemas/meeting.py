from datetime import datetime

from pydantic import BaseModel
from typing import Optional, TYPE_CHECKING

if TYPE_CHECKING:
    from app.schemas.user import UserShort


class MeetCreate(BaseModel):
    date: datetime
    participants: list[str]


class MeetRead(BaseModel):
    id: int
    participants: list["UserShort"]
    canceled: Optional[bool] = None

    class Config:
        from_attributes=True


from app.schemas.user import UserShort
MeetRead.model_rebuild()
