from datetime import datetime

from pydantic import BaseModel


class MeetCreate(BaseModel):
    date: datetime
    participants: list[str]
