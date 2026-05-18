import os

from dotenv import load_dotenv

from sqlalchemy.orm import DeclarativeBase
from fastapi.templating import Jinja2Templates


class Base(DeclarativeBase): ...


load_dotenv()

SECRET_KEY = os.getenv("SECRET_KEY")

smtp_server = os.getenv("EMAIL_SERVER")
smtp_port = os.getenv("EMAIL_PORT")
email_address = os.getenv("EMAIL")
email_password = os.getenv("EMAIL_PASSWORD")

templates = Jinja2Templates(directory="app/templates")

templates.env.globals.update(LOGOUT="http://127.0.0.1:8000/logout")
templates.env.globals.update(LOGIN="http://127.0.0.1:8000/login")
