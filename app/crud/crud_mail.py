import datetime
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import os
import smtplib
from fastapi import HTTPException, Response
from jose import jwt
from jinja2 import (
    Environment,
    FileSystemLoader,
    select_autoescape,
)
from app.core.config import settings
from app.models.user import User, UserCreate


env = Environment(
    loader=FileSystemLoader("app/static/html"), autoescape=select_autoescape()
)


def send_email(recipient: User, msg_data: dict):
    """Send an email to a user.

    Args:
        recipient: object of type User.
        msg_data: dict {'subject': str, 'body': str}
    Returns:
        the square root of n.
    Raises:
        TypeError: if n is not a number.
        ValueError: if n is negative.

    """
    # Error handling
    if not all(
        [
            recipient,
            recipient.email,
            msg_data,
            msg_data.get("subject"),
            msg_data.get("body"),
        ]
    ):
        raise HTTPException(status_code=400)

    # Set up the sender and receiver email addresses
    sender_email = os.getenv("SMTP_LOGIN_MAIL")
    receiver_email = recipient.email
    # Set up the email content
    message = MIMEMultipart()
    message["From"] = sender_email
    message["To"] = receiver_email
    message["Subject"] = msg_data.get("subject")

    # Add email body
    body = msg_data.get("body")
    message.attach(MIMEText(body, "html"))

    # Set up the SMTP server details
    smtp_server = "smtp.abv.bg"
    smtp_port = 465

    # Log in to the SMTP server using your abv.bg email account
    username = settings.SMTP_USER
    password = settings.SMTP_PASSWORD
    server = smtplib.SMTP_SSL(smtp_server, smtp_port)
    server.login(username, password)

    # Send the email and close the SMTP connection
    server.sendmail(sender_email, receiver_email, message.as_string())
    server.quit()

    return Response(status_code=200, content="Email sent successfully!")


def registration_mail(user: UserCreate, user_id: str):
    template = env.get_template("email_verify.html")
    return {
        "subject": "Account confirmation",
        "body": template.render(
            user=user.username, link=f"{settings.SERVER_HOST}/confirm?id={user_id}"
        ),
    }
