import uuid

from fastapi import APIRouter, Request, Depends
from fastapi_users import FastAPIUsers
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.security import OAuth2PasswordRequestForm

from app.auth.auth import auth_backend, auth_backend_cookie
from app.auth.manager import get_user_manager, get_user_manager_context
from app.config import templates
from app.models import UserModel as User, UserModel
from app.schemas import UserRead, UserCreate, UserUpdate

fastapi_user = FastAPIUsers[User, uuid.UUID](
    get_user_manager,
    [auth_backend],
)

auth_router = APIRouter()

auth_router.include_router(
    fastapi_user.get_auth_router(auth_backend_cookie, requires_verification=True),
    prefix="/auth/cookie",
    tags=["auth-frontend"],
)

auth_router.include_router(
    fastapi_user.get_auth_router(auth_backend, requires_verification=True),
    prefix="/auth/jwt",
    tags=["auth"],
)


@auth_router.get("/login", response_class=HTMLResponse)
async def get_login_page(request: Request):
    return templates.TemplateResponse(
        request=request,  # Передаем request явно
        name="login.html",  # Имя файла шаблона
        context={},
    )


# 2. POST: Обрабатываем чистый HTML-форм сабмит
@auth_router.post("/login")
async def login_submit(
    request: Request,
    form_data: OAuth2PasswordRequestForm = Depends(),
):
    try:

        async with get_user_manager_context() as user_manager:
            user = await user_manager.authenticate(credentials=form_data)

        if user is None or not user.is_active:
            raise Exception("Неверные учетные данные")

        strategy = auth_backend_cookie.get_strategy()
        token = await strategy.write_token(user)

        response = await auth_backend_cookie.transport.get_login_response(token)

        response.status_code = 303
        response.headers["Location"] = "/calendar"

        return response

    except Exception as e:
        print(f"❌ ОШИБКА АВТОРИЗАЦИИ: {e}")
        return templates.TemplateResponse(
            request=request,
            name="login.html",
            context={"error": "Неверный логин или пароль"},
        )


@auth_router.get("/logout")
async def logout():
    try:

        response = await auth_backend_cookie.transport.get_logout_response()

        response.status_code = 303

        response.headers["Location"] = "/"

        return response

    except Exception as e:
        print(f"ОШИБКА ВЫХОДА: {e}")
        return RedirectResponse(url="/login", status_code=303)


auth_router.include_router(
    fastapi_user.get_register_router(UserRead, UserCreate),
    prefix="/auth/register",
    tags=["auth"],
)

auth_router.include_router(
    fastapi_user.get_verify_router(UserRead),
    prefix="/auth/verify",
    tags=["auth"],
)

auth_router.include_router(
    fastapi_user.get_reset_password_router(),
    prefix="/auth/reset",
    tags=["auth"],
)

auth_router.include_router(
    fastapi_user.get_users_router(UserRead, UserUpdate),
    prefix="/auth/users",
    tags=["users"],
)
