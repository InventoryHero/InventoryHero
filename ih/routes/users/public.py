from fastapi import APIRouter, HTTPException
from fastapi_utils.cbv import cbv
from starlette import status


from ih.schema.user.user import UserCreate, ResetPasswordForm, TokenValidationResponse, ChangePasswordFormBase, \
    ResetPasswordResponse
from ih.routes._base.PublicControllerBase import PublicControllerBase

router = APIRouter(prefix="/user", tags=["register"])

@cbv(router)
class UserPublicController(PublicControllerBase):
    @router.post("/register", status_code=status.HTTP_204_NO_CONTENT)
    def register_user(self, user: UserCreate):
        if self.user:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail=self.localizer.t('already_authenticated')
            )

        if not self.settings.IH_REGISTRATION_ALLOWED:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail=self.localizer.t('registration_disabled')
            )


        assert not getattr(user, "admin", False), "Public registration cannot set admin=True"
        self.repositories.users.register(user)


    @router.post("/reset-password", status_code=status.HTTP_204_NO_CONTENT)
    async def reset_password(self, email: ResetPasswordForm):
        self.repositories.users.request_password_reset(email.email)

    @router.post("/confirm-email/{code}", status_code=status.HTTP_204_NO_CONTENT)
    def confirm_email(self, code: str):
        self.repositories.users.confirm_email(code)

    @router.get("/validate-password-token/{code}", response_model=TokenValidationResponse, status_code=status.HTTP_200_OK)
    def validate_password_token(self, code: str) -> TokenValidationResponse:
        valid = self.repositories.users.validate_password_token(code)
        return TokenValidationResponse(valid=valid, reason=self.localizer.t('password_reset.invalid_token') if not valid else None)

    @router.post("/reset-password/{code}", response_model=ResetPasswordResponse, status_code=status.HTTP_200_OK)
    def reset_password_with_code(self, code: str, payload: ChangePasswordFormBase):
        success, reason = self.repositories.users.reset_password(code, payload)
        return ResetPasswordResponse(valid=success, reason=reason)

