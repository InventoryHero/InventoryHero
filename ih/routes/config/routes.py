import json
from http.client import HTTPException
from pathlib import Path

from fastapi import APIRouter, Depends

from fastapi_utils.cbv import cbv
from starlette import status
from starlette.responses import JSONResponse

from ih.core.config import get_app_settings
from ih.i18n import get_localizer
from ih.i18n.localizer import Localizer
from ih.routes._base.ControllerBase import ControllerBase
from ih.schema.config import ConfigPublic

router = APIRouter(prefix="")
TRANSLATION_DIR = Path(__file__).resolve().parent.parent.parent / "locales"

@cbv(router)
class ConfigController(ControllerBase):

    @router.get("/", response_model=ConfigPublic, status_code=status.HTTP_200_OK)
    def get_config(self):
        app_settings = get_app_settings()

        return ConfigPublic(
            smtp_enabled=app_settings.IH_SMTP_ENABLED,
            registration_allowed=app_settings.IH_REGISTRATION_ALLOWED
        )
