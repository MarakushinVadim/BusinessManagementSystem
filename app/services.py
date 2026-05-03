from fastapi import HTTPException, status

import smtplib
import socket
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

from loguru import logger

from app.config import smtp_server, smtp_port, email_address, email_password
from app.models import TaskModel


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


def check_current_task_exist(task: TaskModel):
    if not task:
        message = "Задача с таким id не найдена"
        logger.error(message)
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=message)
