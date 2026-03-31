import os

from dotenv import load_dotenv

from sqlalchemy.orm import DeclarativeBase


class Base(DeclarativeBase): ...


load_dotenv()

SECRET_KEY = os.getenv("SECRET_KEY")

smtp_server = os.getenv("EMAIL_SERVER")
smtp_port = os.getenv("EMAIL_PORT")
email_address = os.getenv("EMAIL")
email_password = os.getenv("EMAIL_PASSWORD")
