import os
import secrets
from dotenv import load_dotenv
from typing import Optional

from pydantic import AnyHttpUrl, BaseSettings, EmailStr

load_dotenv()


class Settings(BaseSettings):
    API_V1_STR: str = "/api/v1"
    SECRET_KEY: str = secrets.token_urlsafe(32)
    # 60 minutes * 24 hours * 8 days = 8 days
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60 * 24 * 8

    SERVER_HOST: str = "91.139.226.224"
    DB_ENGINE_URI: str = os.getenv("DB_ENGINE")

    PROJECT_NAME: str = "Kinti prani"

    SMTP_PORT: Optional[int] = 465
    SMTP_HOST: Optional[str] = "smtp.abv.bg"
    SMTP_USER: Optional[str] = os.getenv("SMTP_LOGIN_MAIL")
    SMTP_PASSWORD: Optional[str] = os.getenv("SMTP_LOGIN_PASS")
    EMAILS_FROM_EMAIL: Optional[EmailStr] = os.getenv("SMTP_LOGIN_MAIL")
    EMAILS_FROM_NAME: Optional[str] = PROJECT_NAME

    EMAIL_RESET_TOKEN_EXPIRE_HOURS: int = 48
    EMAIL_TEMPLATES_DIR: str = "app/email-templates/build"

    CURRENCY_REQUEST_URL = os.getenv("CURRENCY_REQUEST_URL")

    class Config:
        case_sensitive = True


settings = Settings()
