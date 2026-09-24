import smtplib
from email.message import EmailMessage

from app.core.settings import settings


def send_email(to: str, subject: str, body: str):
    msg = EmailMessage()
    msg.set_content(body)
    msg["Subject"] = subject
    msg["From"] = settings.MAIL_FROM
    msg["To"] = to

    server = smtplib.SMTP(settings.MAIL_HOST, settings.MAIL_PORT)
    server.send_message(msg)
    server.quit()
