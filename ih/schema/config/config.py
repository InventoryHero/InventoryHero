from typing import Optional

from pydantic import BaseModel


class ConfigPublic(BaseModel):
    smtp_enabled: bool
    registration_allowed: bool


class AppConfig(BaseModel):
    smtp_enabled: bool
    registration_allowed: bool
    app_version: str
    base_url: str
    base_url_default: bool
    database_type: str
    database_connection: str
    oidc_enabled: bool
    deployment: str

