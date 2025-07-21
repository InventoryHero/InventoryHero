from pydantic import BaseModel


class ConfigPublic(BaseModel):
    smtp_enabled: bool
    registration_allowed: bool