import logging
from pathlib import Path

from pydantic_settings import BaseSettings

from ih.core.settings.provider import Provider, db_factory
from ih.db.models.User import User


class AppSettings(BaseSettings):
    #STATIC_FILES: str =

    IH_DEMO: bool = False

    HOST_IP: str = "*"
    HOST: str = "0.0.0.0"
    PORT: int = 5000
    API_DOCS: bool = True

    IH_APP_URL: str = f"http://{HOST}:{PORT}"

    IH_ACCESS_TOKEN_EXPIRATION: int = 15 * 60
    IH_REFRESH_TOKEN_EXPIRATION: int = 3600 * 24 * 7

    IH_SECRET_KEY: str = "mysupersecretstring"

    IH_REGISTRATION_ALLOWED: bool = False

    IH_DB_ENGINE: str = "sqlite"

    IH_SMTP_HOST: str|None = None
    IH_SMTP_PORT: int | None = None
    IH_SMTP_USER: str | None = None
    IH_SMTP_PASSWORD: str | None = None
    IH_SMTP_FROM_NAME: str | None = None
    IH_SMTP_FROM_EMAIL: str | None = None
    IH_SMTP_AUTH_METHOD: str | None = "NONE"


    DB_PROVIDER: Provider | None = None

    PRODUCTION: bool = True
    TESTING: bool = False

    @property
    def DB_URL(self) -> str | None:
        return self.DB_PROVIDER.db_url if self.DB_PROVIDER else None

    @property
    def IH_SMTP_ENABLED(self) -> bool:
        # TODO AUTH METHOD CHECKING ETC

        return self.IH_SMTP_HOST is not None and self.IH_SMTP_PORT is not None and self.IH_SMTP_FROM_NAME is not None and self.IH_SMTP_FROM_EMAIL is not None

    @property
    def LOG_LEVEL(self) -> int:
        if self.PRODUCTION:
            return logging.WARNING
        if self.TESTING:
            return logging.INFO
        return logging.DEBUG



    _IH_DEFAULT_USERNAME: str = "admin"
    _IH_DEFAULT_EMAIL: str = "changeme@change.me"
    _IH_DEFAULT_PASSWORD: str = "changeme"



def build_app_settings(env_file: Path,  data_dir: Path) -> AppSettings:
    app_settings = AppSettings()
    app_settings.DB_PROVIDER = db_factory(
        app_settings.IH_DB_ENGINE or "sqlite",
        data_dir,
        env_file=env_file,
    )
    return app_settings