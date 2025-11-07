
from pathlib import Path

from fastapi import APIRouter, Depends

from fastapi_utils.cbv import cbv
from starlette import status

from ih.core.exceptions.exceptions import InventoryHeroAPIException
from ih.routes._base.AdminControllerBase import BaseAdminController
from ih.routes._base.ControllerBase import ControllerBase
from ih.routes._base.AdminApiRouter import AdminAPIRouter
from ih.schema.common.error_response import ErrorResponse
from ih.schema.config import ConfigPublic, AppConfig
from ih.services.email.email import send_test_email

router = APIRouter(prefix="")
admin_router = AdminAPIRouter(prefix="")


@cbv(router)
class ConfigController(ControllerBase):

    @router.get("/", response_model=ConfigPublic, status_code=status.HTTP_200_OK)
    def get_config(self):

        return ConfigPublic(
            smtp_enabled=self.settings.IH_SMTP_ENABLED,
            registration_allowed=self.settings.IH_REGISTRATION_ALLOWED,
            oidc_enabled=self.settings.OIDC.enabled,
            oidc_name=self.settings.OIDC.IH_OIDC_NAME,
        )

@cbv(admin_router)
class AdminConfigController(BaseAdminController):
    @admin_router.get("/", response_model=AppConfig, status_code=status.HTTP_200_OK)
    def get_app_config(self):
        return AppConfig(
            smtp_enabled=self.settings.IH_SMTP_ENABLED,
            registration_allowed=self.settings.IH_REGISTRATION_ALLOWED,
            app_version=self.settings.IH_APP_VERSION,
            base_url=self.settings.IH_APP_URL,
            base_url_default=not self.settings.IH_APP_URL_SET,
            database_type=self.settings.DB_PROVIDER.db_type,
            database_connection=self.settings.DB_PROVIDER.db_url_public,
            deployment=self.localizer.t('deployment.production') if self.settings.PRODUCTION else self.localizer.t('deployment.development'),
            oidc_enabled=self.settings.OIDC.enabled
        )

    @admin_router.post("/email/test", status_code=status.HTTP_204_NO_CONTENT)
    def send_test_email(self, email: str):
        self.logger.info(f"Sending test email to {email}")
        if not send_test_email(email):
            raise InventoryHeroAPIException(
                status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
                detail=ErrorResponse(
                    message="",
                    toast=False
                )
            )
        pass
