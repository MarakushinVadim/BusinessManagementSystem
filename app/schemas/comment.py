from datetime import datetime

from pydantic import BaseModel

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from app.schemas.user import UserShort


class CommentCreate(BaseModel):
    text: str

class CommentOut(BaseModel):
    id: int
    text: str
    author: "UserShort"
    created_at: datetime
    class Config: from_attributes = True

from app.schemas.user import UserShort
CommentOut.model_rebuild()
