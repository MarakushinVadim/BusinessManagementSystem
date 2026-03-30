from typing import Optional

from app.models.user import RoleType

import uuid

from fastapi_users import schemas


class UserRead(schemas.BaseUser[uuid.UUID]):
    role: Optional[RoleType] = None


class UserCreate(schemas.BaseUserCreate):
    role: Optional[RoleType] = "user"


class UserUpdate(schemas.BaseUserUpdate):
    role: Optional[RoleType] = None
