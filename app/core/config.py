from typing import Optional, Union
from pydantic import AnyHttpUrl, BaseSettings, EmailStr, Field


class Settings(BaseSettings):
    PROJECT_NAME: str = "Kache"

    API_V1_STR: str = "/api/v1"

    SECRET_KEY: str = Field(default="secret", env="SECRET_KEY")
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60 * 24 * 8

    # SERVER_HOST: str = "http://91.139.226.224"
    SERVER_HOST: str = "http://localhost:8000"
    DB_ENGINE_URI: str = Field(default="", env="DB_ENGINE")

    # EMAIL SETTINGS
    SMTP_PORT: Optional[int] = 465
    SMTP_HOST: Optional[str] = "smtp.abv.bg"
    SMTP_USER: Optional[str] = Field(default="", env="SMTP_LOGIN_MAIL")
    SMTP_PASSWORD: Optional[str] = Field(default="", env="SMTP_LOGIN_PASS")

    EMAILS_FROM_EMAIL: Optional[EmailStr] = Field(default="", env="SMTP_LOGIN_MAIL")
    EMAILS_FROM_NAME: Optional[str] = PROJECT_NAME
    EMAIL_RESET_TOKEN_EXPIRE_HOURS: int = 48
    EMAIL_TEMPLATES_DIR: str = "app/email-templates/build"

    # APIs
    CURRENCY_REQUEST_URL = Field(default="", env="CURRENCY_REQUEST_URL")

    # TESTING
    ADMIN_TEST_USERNAME: str = "adminUser"
    ADMIN_TEST_PASSWORD: str = "AdminPass_1"
    ADMIN_TEST_EMAIL: str = "adminUser@example.com"
    USER_TEST_USERNAME: str = "normalUser"
    USER_TEST_PASSWORD: str = "UserPass_1"
    USER_TEST_EMAIL: str = "normalUser@example.com"

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"
        case_sensitive = True


settings = Settings()
