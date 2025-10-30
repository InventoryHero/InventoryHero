import logging
from pathlib import Path

from pydantic_settings import BaseSettings

from ih.core.settings.provider import Provider, db_factory
from ih.db.models.User import User


class AppSettings(BaseSettings):
    IH_APP_URL: str = "https://localhost:3000"

    # TODO LET FASTAPI SERVE STATIC FILES IN DOCKER
    #STATIC_FILES: str =

    IH_DEMO: bool = False

    HOST_IP: str = "*"
    API_HOST: str = "0.0.0.0"
    API_PORT: int = 5000
    API_DOCS: bool = True

    IH_ACCESS_TOKEN_EXPIRATION: int = 15
    IH_REFRESH_TOKEN_EXPIRATION: int = 3600 * 24 * 7

    IH_SECRET_KEY: str = "mysupersecretstring"
    #SESSION_SECRET: str

    IH_REGISTRATION_ALLOWED: bool = False

    IH_DB_ENGINE: str = "sqlite"
    DB_PROVIDER: Provider | None = None

    PRODUCTION: bool = True
    TESTING: bool = False

    @property
    def DB_URL(self) -> str | None:
        return self.DB_PROVIDER.db_url if self.DB_PROVIDER else None

    @property
    def IH_SMTP(self) -> None:
        # TODO IMPLEMENT SMTP
        return None

    @property
    def IH_SMTP_ENABLED(self) -> bool:
        return self.IH_SMTP is not None

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