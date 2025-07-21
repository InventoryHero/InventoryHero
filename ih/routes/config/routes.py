from fastapi import APIRouter, Depends

from fastapi_utils.cbv import cbv
from starlette import status

from ih.core.config import get_app_settings
from ih.routes._base.ControllerBase import ControllerBase
from ih.schema.config import ConfigPublic

router = APIRouter(prefix="")

@cbv(router)
class ConfigController(ControllerBase):
    @router.get("/", response_model=ConfigPublic, status_code=status.HTTP_200_OK)
    def get_config(self):
        app_settings = get_app_settings()
        return ConfigPublic(
            smtp_enabled=app_settings.IH_SMTP_ENABLED,
            registration_allowed=app_settings.IH_REGISTRATION_ALLOWED
        )