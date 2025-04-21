from fastapi import APIRouter, HTTPException
from fastapi_utils.cbv import cbv
from starlette import status

from ih.schema.user.user import UserCreate
from ih.routes._base.PublicControllerBase import PublicControllerBase

router = APIRouter(prefix="/register", tags=["register"])

@cbv(router)
class RegisterController(PublicControllerBase):
    @router.post("/", status_code=status.HTTP_201_CREATED)
    def register_user(self, user: UserCreate):
        if self.user:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="already_authenticated"
            )

        if not self.settings.IH_REGISTRATION_ALLOWED:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="registration_disabled"
            )

        assert not getattr(user, "admin", False), "Public registration cannot set admin=True"
        self.repositories.users.create(user)
        return