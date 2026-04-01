from app.models.user import UserModel as User
from sqladmin import ModelView


class UserAdminView(ModelView, model=User):
    column_list = [User.id, User.email, User.role, User.is_active]
    column_searchable_list = [User.email]
    column_filters = [User.role, User.is_active]
    name = "Пользователь"
    name_plural = "Пользователи"
    icon = "fa-solid fa-user"

    form_excluded_columns = [User.hashed_password]
