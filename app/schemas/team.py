import uuid

from pydantic import BaseModel

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from app.schemas.user import UserShort


class TeamCreate(BaseModel):
    users: list[uuid.UUID]
    title: str


class TeamRead(BaseModel):
    id: int
    title: str
    users: list["UserShort"]

    class Config:
        from_attributes = True


from app.schemas.user import UserShort

TeamRead.model_rebuild()
