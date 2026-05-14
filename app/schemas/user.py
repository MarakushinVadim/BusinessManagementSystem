from typing import Optional

from app.models.user import RoleType

import uuid

from fastapi_users import schemas

from pydantic import computed_field, BaseModel


class UserRead(schemas.BaseUser[uuid.UUID]):
    role: Optional[RoleType] = None

class UserShort(BaseModel):
    id: uuid.UUID
    name: Optional[str] = None
    surname: Optional[str] = None
    email: str

    @computed_field
    @property
    def display_name(self) -> str:
        if self.name and self.surname:
            return f"{self.name} {self.surname}"
        elif self.name:
            return f"{self.name}"
        elif self.surname:
            return f"{self.surname}"
        return f"{self.email}"

    class Config:
        from_attributes=True


class UserCreate(schemas.BaseUserCreate):
    role: Optional[RoleType] = "user"


class UserUpdate(schemas.BaseUserUpdate):
    role: Optional[RoleType] = None
    name: Optional[str] = None
    surname: Optional[str] = None
