from typing import Optional

from app.models.user import RoleType

import uuid

from fastapi_users import schemas

from pydantic import BaseModel


class UserRead(schemas.BaseUser[uuid.UUID]):
    role: Optional[RoleType] = None


class UserCreate(schemas.BaseUserCreate):
    role: Optional[RoleType] = "user"


class UserUpdate(schemas.BaseUserUpdate):
    role: Optional[RoleType] = None

class UserShort(BaseModel):
    id: uuid.UUID
    username: str
    class Config: from_attributes = True
