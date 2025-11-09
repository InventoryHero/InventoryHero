import logging
from pathlib import Path

from pydantic_settings import BaseSettings

from ih.core.settings.provider import Provider, db_factory
from ih.core.settings.oidc import OidcSettings
from ih import __version__



class AppSettings(BaseSettings):
    IH_DEMO: bool = False

    HOST_IP: str = "*"
    HOST: str = "0.0.0.0"
    PORT: int = 5000
    API_DOCS: bool = True

    _IH_APP_URL: str = f"http://{HOST}:{PORT}"
    IH_APP_URL: str = _IH_APP_URL

    IH_ACCESS_TOKEN_EXPIRATION: int = 15 * 60
    IH_REFRESH_TOKEN_EXPIRATION: int = 3600 * 24 * 7

    IH_SECRET_KEY: str = "mysupersecretstring"

    IH_REGISTRATION_ALLOWED: bool = False

    IH_DB_ENGINE: str = "sqlite"

    IH_SMTP_HOST: str|None = None
    IH_SMTP_PORT: int | None = None
    IH_SMTP_USERNAME: str | None = None
    IH_SMTP_PASSWORD: str | None = None
    IH_SMTP_FROM_NAME: str | None = None
    IH_SMTP_FROM_EMAIL: str | None = None
    IH_SMTP_AUTH_METHOD: str | None = "NONE"

    DB_PROVIDER: Provider | None = None

    OIDC: OidcSettings | None = None

    PROFILE_PICTURE_DATA_DIR: Path | None = None
    ALLOWED_IMAGE_TYPES: list[str] | None = None

    PRODUCTION: bool = True
    TESTING: bool = False

    @property
    def DB_URL(self) -> str | None:
        return self.DB_PROVIDER.db_url if self.DB_PROVIDER else None

    @property
    def IH_SMTP_ENABLED(self) -> bool:

        if self.IH_SMTP_AUTH_METHOD.upper() == "NONE":
            return all([
                self.IH_SMTP_HOST,
                self.IH_SMTP_PORT,
                self.IH_SMTP_FROM_NAME,
                self.IH_SMTP_FROM_EMAIL,
            ])

        if self.IH_SMTP_AUTH_METHOD.upper() not in ["TLS", "SSL"]:
            return False


        return all([
            self.IH_SMTP_HOST,
            self.IH_SMTP_PORT,
            self.IH_SMTP_FROM_NAME,
            self.IH_SMTP_FROM_EMAIL,
            self.IH_SMTP_USERNAME,
            self.IH_SMTP_PASSWORD
        ])

    @property
    def IH_SMTP_USE_SSL(self) -> bool:
        return self.IH_SMTP_AUTH_METHOD.upper() == "SSL"

    @property
    def IH_SMTP_USE_TLS(self) -> bool:
        return self.IH_SMTP_AUTH_METHOD.upper() == "TLS"

    @property
    def LOG_LEVEL(self) -> int:
        if self.PRODUCTION:
            return logging.WARNING
        if self.TESTING:
            return logging.INFO

        return logging.DEBUG

    @property
    def IH_APP_VERSION(self) -> str:
        return __version__

    @property
    def IH_APP_URL_SET(self) -> bool:
        return self.IH_APP_URL != self._IH_APP_URL



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
    app_settings.OIDC = OidcSettings()
    app_settings.PROFILE_PICTURE_DATA_DIR = data_dir / "ProfilePictures"
    app_settings.PROFILE_PICTURE_DATA_DIR.mkdir(parents=True, exist_ok=True)
    app_settings.ALLOWED_IMAGE_TYPES = [
        "image/jpeg",
        "image/png",
        "image/webp",
        "image/bmp",
        "image/tiff",
        # Note: SVG is vector, Pillow cannot handle SVG directly
    ]
    return app_settings