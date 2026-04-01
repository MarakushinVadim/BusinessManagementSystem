from fastapi_users.authentication import (
    AuthenticationBackend,
    BearerTransport,
    JWTStrategy,
)
from sqladmin.authentication import AuthenticationBackend as AdminAuthBack
from starlette.requests import Request
from starlette.responses import Response

from app.config import SECRET_KEY
from app.auth.manager import get_user_manager_context

SECRET = SECRET_KEY

bearer_transport = BearerTransport(tokenUrl="auth/jwt/login")


def get_jwt_strategy() -> JWTStrategy:
    return JWTStrategy(secret=SECRET, lifetime_seconds=3600)


auth_backend = AuthenticationBackend(
    name="jwt",
    transport=bearer_transport,
    get_strategy=get_jwt_strategy,
)


class AdminAuth(AdminAuthBack):
    async def login(self, request: Request) -> bool:
        form = await request.form()
        email, password = form.get("username"), form.get("password")

        async with get_user_manager_context() as user_manager:
            try:
                user = await user_manager.get_by_email(email)
            except Exception:
                return False

            is_valid, _ = user_manager.password_helper.verify_and_update(
                password, user.hashed_password
            )

            if is_valid and user.is_active and str(user.role) == "admin":
                strategy = get_jwt_strategy()
                token = await strategy.write_token(user)

                request.session.update({"token": token})
                return True
        return False

    async def logout(self, request: Request) -> bool:
        request.session.clear()
        return True

    async def authenticate(self, request: Request) -> bool:
        token = request.session.get("token")
        if not token:
            return False

        strategy = get_jwt_strategy()
        async with get_user_manager_context() as user_manager:
            user = await strategy.read_token(token, user_manager)

            if user and user.is_active and user.role == "admin":
                return True

        return False


admin_authentication_backend = AdminAuth(secret_key=SECRET_KEY)
