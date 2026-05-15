from datetime import datetime

from pydantic import BaseModel
from typing import Optional, TYPE_CHECKING, Literal

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
        from_attributes = True


class MeetShort(BaseModel):
    id: int
    title: Optional[str] = None
    date: datetime
    canceled: Optional[bool] = None


MeetTuple = tuple[Literal["meets"], list[MeetShort]]


from app.schemas.user import UserShort

MeetRead.model_rebuild()
