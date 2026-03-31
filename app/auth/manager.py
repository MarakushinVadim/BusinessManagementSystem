import uuid

from fastapi import Depends, Request
from fastapi_users import BaseUserManager, UUIDIDMixin
from app.models import UserModel as User
from app.database import get_user_db
from app.config import SECRET_KEY
from loguru import logger

from app.services import email_sender

SECRET = SECRET_KEY


class UserManager(UUIDIDMixin, BaseUserManager[User, uuid.UUID]):
    reset_password_token_secret = SECRET
    verification_token_secret = SECRET

    async def on_after_register(self, user: User, request: Request | None = None):
        token = await self.request_verify(user, request)

        logger.info(f"User {user.id} has registered. Verification token: {token}")

    async def on_after_forgot_password(
        self, user: User, token: str, request: Request | None = None
    ):
        logger.info(
            f"Пользователь {user.id} забыл пароль. Токен для сброса пароля: {token}"
        )

    async def on_after_request_verify(
        self, user: User, token: str, request: Request | None = None
    ):
        message = await email_sender.create_message(user.email, token)
        await email_sender.send_mail(message)

        logger.info(
            f"Поступил запрос на верификацию от пользователя {user.id}. Токен: {token}"
        )

    async def on_after_verify(self, user: User, request: Request | None = None) -> None:
        logger.info(f"Пользователь {user.id} верифицирован!")


async def get_user_manager(user_db=Depends(get_user_db)):
    yield UserManager(user_db)
