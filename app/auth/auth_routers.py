import uuid

from fastapi import APIRouter
from fastapi_users import FastAPIUsers

from app.auth.auth import auth_backend
from app.auth.manager import get_user_manager
from app.models import UserModel as User
from app.schemas import UserRead, UserCreate, UserUpdate

fastapi_users = FastAPIUsers[User, uuid.UUID](
    get_user_manager,
    [auth_backend],
)

auth_router = APIRouter()

auth_router.include_router(
    fastapi_users.get_auth_router(auth_backend, requires_verification=True),
    prefix="/auth/jwt",
    tags=["auth"],
)

auth_router.include_router(
    fastapi_users.get_register_router(UserRead, UserCreate),
    prefix="/auth/register",
    tags=["auth"],
)

auth_router.include_router(
    fastapi_users.get_verify_router(UserRead),
    prefix="/auth/verify",
    tags=["auth"],
)

auth_router.include_router(
    fastapi_users.get_reset_password_router(),
    prefix="/auth/reset",
    tags=["auth"],
)

auth_router.include_router(
    fastapi_users.get_users_router(UserRead, UserUpdate),
    prefix="/auth/users",
    tags=["users"],
)
