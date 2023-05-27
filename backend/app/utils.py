from datetime import datetime, timedelta
from typing import Any, Dict, Optional
from snowflake import SnowflakeGenerator, Snowflake
from emails.template import JinjaTemplate
from pathlib import Path
from jose import jwt

import requests
import emails
import random

from sqlmodel import Session
from app.core import settings

from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.primitives import padding
import base64

from app.models import Currency, User


class EmailUtility:
    def __init__(self):
        pass

    def send_email(
        self,
        email_to: str,
        subject_template: str = "",
        html_template: str = "",
        environment: Dict[str, Any] = {},
    ) -> None:
        message = emails.Message(
            subject=JinjaTemplate(subject_template),
            html=JinjaTemplate(html_template),
            mail_from=(settings.EMAILS_FROM_NAME, settings.EMAILS_FROM_EMAIL),
        )
        smtp_options = {
            "host": settings.SMTP_HOST,
            "port": settings.SMTP_PORT,
            "ssl": True,
        }

        if settings.SMTP_USER:
            smtp_options["user"] = settings.SMTP_USER
        if settings.SMTP_PASSWORD:
            smtp_options["password"] = settings.SMTP_PASSWORD

        response = message.send(to=email_to, render=environment, smtp=smtp_options)

    def send_test_email(self, email_to: str) -> None:
        project_name = settings.PROJECT_NAME
        subject = f"{project_name} - Test email"
        with open(Path(f"{settings.EMAIL_TEMPLATES_DIR}/test_email.html")) as f:
            template_str = f.read()
        self.send_email(
            email_to=email_to,
            subject_template=subject,
            html_template=template_str,
            environment={"project_name": settings.PROJECT_NAME, "email": email_to},
        )

    def send_reset_password_email(self, email_to: str, email: str, token: str) -> None:
        project_name = settings.PROJECT_NAME
        subject = f"{project_name} - Password recovery"
        with open(Path(settings.EMAIL_TEMPLATES_DIR) / "reset_password.html") as f:
            template_str = f.read()
        server_host = settings.SERVER_HOST
        link = f"{server_host}/reset-password?token={token}"
        self.send_email(
            email_to=email_to,
            subject_template=subject,
            html_template=template_str,
            environment={
                "project_name": settings.PROJECT_NAME,
                "username": email,
                "email": email_to,
                "valid_hours": settings.EMAIL_RESET_TOKEN_EXPIRE_HOURS,
                "link": link,
            },
        )

    def send_new_account_email(self, email_to: str, username: str) -> None:
        project_name = settings.PROJECT_NAME
        subject = f"{project_name} - New account for user {username}"
        token = self.generate_email_link_token(email_to)
        with open(Path(settings.EMAIL_TEMPLATES_DIR) / "new_account.html") as f:
            template_str = f.read()
        link = f"{settings.SERVER_HOST}{settings.API_V1_STR}/users/verify/{token}"
        self.send_email(
            email_to=email_to,
            subject_template=subject,
            html_template=template_str,
            environment={
                "project_name": settings.PROJECT_NAME,
                "username": username,
                "email": email_to,
                "link": link,
            },
        )

    def send_refferal_email(self, email_to: str, refferer: User):
        # Needs a new html done and the link needs to connect to the client server
        project_name = settings.PROJECT_NAME
        refferer_fullname = f"{refferer.f_name} {refferer.l_name}"

        subject = (
            f"{project_name} - You have been invited to join from {refferer_fullname}"
        )

        token = self.generate_email_link_token(refferer.email)
        with open(Path(settings.EMAIL_TEMPLATES_DIR) / "new_account.html") as f:
            template_str = f.read()
        link = f"{settings.SERVER_HOST}{settings.API_V1_STR}/signup?referrer={token}"
        self.send_email(
            email_to=email_to,
            subject_template=subject,
            html_template=template_str,
            environment={
                "project_name": settings.PROJECT_NAME,
                "username": refferer_fullname,
                "email": email_to,
                "link": link,
            },
        )

    def generate_email_link_token(self, email: str) -> str:
        delta = timedelta(hours=settings.EMAIL_RESET_TOKEN_EXPIRE_HOURS)
        now = datetime.utcnow()
        expires = now + delta
        exp = expires.timestamp()
        encoded_jwt = jwt.encode(
            {"exp": exp, "nbf": now, "sub": email},
            settings.SECRET_KEY,
            algorithm=settings.ALGORITHM,
        )
        return encoded_jwt

    def verify_email_link_token(self, token: str) -> Optional[str]:
        try:
            decoded_token = jwt.decode(
                token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM]
            )
            return decoded_token["sub"]
        except jwt.JWTError:
            return None


class IDUtility:
    def __init__(self):
        pass

    def generate_id(self) -> str:
        """Generates a unique identifier.

        Returns:
            str: 19 digits in a str format
        """
        instance = random.choice(range(1, 1024))
        return str(next(SnowflakeGenerator(instance)))

    def datetime_from_id(self, id: str) -> datetime:
        """Parses a snowflake ID and retrieves the datetime from it in UTC

        Args:
            id: str
        Returns:
            datetime: when the ID was issued
        """
        return Snowflake.parse(int(id)).datetime


class CurrencyExchangeUtility:
    def __init__(self):
        pass

    def _get_all_rates(self) -> dict:
        """
        Gets the rates of all supported currencies.

        Returns:
            dict: keys of which are the currencies - 'USD', 'BGN' etc.
        """

        data = requests.get(settings.CURRENCY_REQUEST_URL)

        data = data.json().get("data")
        return data

    def _write_rates_to_db(self, db: Session):
        data = self._get_all_rates()
        rates = []
        for curr, rate in data.items():
            rates.append(Currency(currency=curr, rate=rate))

        db.exec("TRUNCATE TABLE currencies")
        db.commit()

        db.add_all(rates)
        db.commit()
        print("DB currency rates refreshed")

    def get_rate(self, data: dict, base_curr: str, to_curr: str) -> float:
        rate = data[to_curr] / data[base_curr]
        return rate

    def exchange(self, rate: float, amount: float):
        return amount * rate


class EncryptUtility:
    def __init__(self):
        self.cipher = Cipher(
            algorithms.AES(base64.b64decode(settings.AES_KEY)),
            modes.CBC(base64.b64decode(settings.CBC_iv)),
        )

    def encrypt(self, input: str) -> str:
        encryptor = self.cipher.encryptor()
        padder = padding.PKCS7(128).padder()
        padded_data = padder.update(input.encode()) + padder.finalize()
        ciphertxt = encryptor.update(padded_data) + encryptor.finalize()
        base_64_str = base64.b64encode(ciphertxt).decode()
        return base_64_str

    def decrypt(self, input: str) -> str:
        decryptor = self.cipher.decryptor()
        ciphertxt = base64.b64decode(input)
        decrypted_padded = decryptor.update(ciphertxt) + decryptor.finalize()
        unpadder = padding.PKCS7(128).unpadder()
        decrypted_data = unpadder.update(decrypted_padded) + unpadder.finalize()
        base_64_str = base64.b64encode(decrypted_data).decode()
        return base64.b64decode(base_64_str).decode()


util_mail = EmailUtility()
util_id = IDUtility()
util_exchange = CurrencyExchangeUtility()
util_crypt = EncryptUtility()
