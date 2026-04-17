from typing import Any

from starlette.requests import Request

from app.models import TaskModel, UserModel, TeamModel
from sqladmin import ModelView


class UserAdminView(ModelView, model=UserModel):
    column_list = [
        UserModel.id,
        UserModel.email,
        UserModel.role,
        UserModel.is_active,
        UserModel.is_verified,
    ]
    column_searchable_list = [UserModel.email, UserModel.role]
    name = "Пользователь"
    name_plural = "Пользователи"
    icon = "fa-solid fa-user"

    form_excluded_columns = [UserModel.hashed_password]

    form_args = {
        "role": {
            "label": "Роль пользователя",
        }
    }


class TaskAdminView(ModelView, model=TaskModel):
    column_list = ["title", "author_id", "performer_id", "deadline", "status"]

    name = "Задача"
    name_plural = "Задачи"
    icon = "fa-solid fa-list-check"

    form_excluded_columns = ["author_id"]

    async def on_model_change(
        self, data: dict, model: Any, is_created: bool, request: Request
    ) -> None:
        if is_created:
            user_id = request.session.get("user_id")
            if user_id:
                data["author_id"] = user_id


class TeamAdminView(ModelView, model=TeamModel):
    column_list = ["id", "admin_id", "users"]

    name = "Команда"
    name_plural = "Команды"
    icon = "ti ti-users-group"
