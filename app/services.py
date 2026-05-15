from fastapi import HTTPException, status

import smtplib
import socket
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

from loguru import logger
from starlette.status import HTTP_400_BAD_REQUEST, HTTP_403_FORBIDDEN

from app.config import smtp_server, smtp_port, email_address, email_password
from app.models import TaskModel, UserModel, MeetingModel

from datetime import datetime, timedelta


class SendMail:
    def __init__(self, smtp_server, smtp_port, email_address, email_password):
        self.smtp_server = smtp_server
        self.smtp_port = smtp_port
        self.email_address = email_address
        self.email_password = email_password

    def check_connection(self):
        try:
            logger.info(f"Connecting to {self.smtp_server}:{self.smtp_port}")
            server = smtplib.SMTP(self.smtp_server, self.smtp_port, timeout=10)

            code, message = server.helo()
            if code == 250:
                logger.info(f"Connection established")
            else:
                logger.info(f"Connection failed {code} {message}")
        except socket.gaierror:
            logger.info("Check smtp_server")
        except ConnectionRefusedError:
            logger.info("Check port")
        except Exception as e:
            logger.info(f"Error connection {e}")

    async def create_message(self, email, token):
        message = MIMEMultipart()
        message["From"] = self.email_address
        message["To"] = email
        message["Subject"] = "Business Management System код верификации"

        body = f"""
            <html>
              <body>
                <p>Добрый день!</p>
                <p>Для подтверждения и активации учетной записи копируйте этот токен: <b>{token}</b></p>
                <p>И вставьте его в поле для верифакации по адресу: <br>https://127.0.0.1:8000//auth/verify/verify/</br></p>
              </body>
            </html>
            """
        message.attach(MIMEText(body, "html"))

        logger.info(f"Сообщение для {email} успешно создано")

        return message

    async def send_mail(self, message: MIMEMultipart) -> None:
        try:
            recipient = message["To"]
            logger.info(f"отправляем сообщение {recipient}")

            server = smtplib.SMTP(self.smtp_server, self.smtp_port)
            server.starttls()
            server.login(self.email_address, self.email_password)

            text = message.as_string()
            server.sendmail(self.email_address, recipient, text)

            logger.info(f"Сообщение успешно отпралено на почту {recipient}")

            server.quit()

        except Exception as e:
            logger.info(f"Произошла ошибка: {e}")


email_sender = SendMail(smtp_server, smtp_port, email_address, email_password)


async def check_current_task_exist(task: TaskModel):
    if not task:
        message = "Задача с таким id не найдена"
        logger.error(message)
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=message)


async def check_author(task: TaskModel, user: UserModel):
    if task.author_id != user.id:
        print("author - ", task.author_id)
        print("user -", user.id)
        message = "Вносить изменения в задачу может только ее автор!"
        logger.error(message)
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=message)


async def check_task_done(task: TaskModel):
    if task.status != "done":
        message = "Оценивать можно только завершенные задачи!"
        logger.error(message)
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=message)


async def check_free_datetime_for_meet(
    date: datetime, user_meet_list: MeetingModel, user: UserModel
):
    if date >= user_meet_list.date and date <= user_meet_list.date + timedelta(hours=1):
        message = f"У пользователя {user.email} есть встреча на это время"
        logger.error(message)
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=message)


async def check_meet(meet: MeetingModel):
    if meet.canceled:
        message = "Встреча уже отменена"
        logger.error(message)
        raise HTTPException(status_code=HTTP_400_BAD_REQUEST, detail=message)


async def check_admin(user: UserModel):
    if not user.role == "admin":
        message = "Этот действие доступно только Администратору"
        logger.error(message)
        raise HTTPException(status_code=HTTP_403_FORBIDDEN, detail=message)


async def check_user_exists(user: UserModel | None):
    if not user:
        message = "Пользователя с таким id не существует"
        logger.error(message)
        raise HTTPException(status_code=HTTP_400_BAD_REQUEST, detail=message)
