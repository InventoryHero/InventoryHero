from datetime import timedelta
from typing import Optional

from PIL import Image
import io
from fastapi import HTTPException, APIRouter, UploadFile, File, Response
from fastapi_utils.cbv import cbv
from starlette import status
import httpx

from uuid import UUID

from starlette.responses import FileResponse, StreamingResponse

from ih.core.exceptions.exceptions import InventoryHeroAPIException
from ih.schema.common.error_response import ErrorResponse
from ih.schema.households import HouseholdSelection, HouseholdWithMemberPublic
from ih.schema.user.user import UserPublic, AdminUserCreate, UserUpdate, ChangePasswordForm, AdminUserUpdate
from ih.routes._base.AdminApiRouter import AdminAPIRouter
from ih.routes._base.AdminControllerBase import BaseAdminController
from ih.routes._base.UserApiRouter import UserAPIRouter
from ih.routes._base.UserControllerBase import UserControllerBase

user_router = UserAPIRouter(
    prefix="/user",
    tags=["user"],
)

public_user_router = APIRouter(
    prefix="/user",
    tags=["user"],
)

admin_router = AdminAPIRouter(
    prefix="/user",
    tags=["user admin"],
)

@cbv(admin_router)
class AdminUserController(BaseAdminController):
    @admin_router.get("/users", response_model=list[UserPublic])
    async def get_all(self):
        return self.repositories.users.get_all()

    @admin_router.post("/create", response_model=UserPublic, status_code=status.HTTP_201_CREATED)
    async def create(self, user: AdminUserCreate):
        return self.repositories.users.create(user)

    @admin_router.get("/{id}", status_code=200, response_model=UserPublic)
    async def get_user(self, id: UUID):
        return self.repositories.users.get_user_by_id(id)

    @admin_router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
    async def delete(self, id: UUID):
        if id == self.user.id:
            raise InventoryHeroAPIException(status_code=status.HTTP_400_BAD_REQUEST, detail=ErrorResponse(
                message = self.localizer.t('self_delete_not_possible'),
                toast = True
            ))

        success: bool = self.repositories.users.delete(id)
        if not success:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=self.localizer.t('delete_not_possible'))

    @admin_router.put("/{user_id}", status_code=200, response_model=UserPublic)
    async def update_user(self, user_id: UUID, to_update: AdminUserUpdate):
        # todo enforce username length backendside (same as email)
        return self.repositories.users.update_user(user_id, to_update)

    @admin_router.put("/{user_id}/reset-password", status_code=status.HTTP_200_OK)
    async def reset_password(self, user_id: UUID):
        return self.repositories.users.request_password_reset_admin(user_id, self.user.username)

    @admin_router.post("/{user_id}/resend-confirmation", status_code=status.HTTP_204_NO_CONTENT)
    async def resend_confirmation(self, user_id: UUID):
        self.repositories.users.resend_confirmation(user_id)



@cbv(user_router)
class UserController(UserControllerBase):

    @user_router.get("/self", response_model=UserPublic)
    async def get_user_details(self):
        return self.user

    @user_router.post("/current-household", response_model=Optional[HouseholdWithMemberPublic], status_code=status.HTTP_200_OK)
    async def set_current_household(self, household: HouseholdSelection):
        return self.repositories.users.set_current_household(household.id)

    @user_router.get("/current-household", response_model=Optional[HouseholdWithMemberPublic], status_code=status.HTTP_200_OK)
    async def get_current_household(self):
        return self.household

    @user_router.put("/self", response_model=UserPublic, status_code=status.HTTP_200_OK)
    async def update_user(self, to_update: UserUpdate):
        return self.repositories.users.update_user(self.user.id, to_update)

    @user_router.post("/change-password", status_code=204)
    async def change_password(self, reset: ChangePasswordForm):
        return self.repositories.users.change_password(self.user.id, reset.current_password, reset.new_password, reset.new_password_confirmation)

    @user_router.get("/request-confirmation", status_code=status.HTTP_204_NO_CONTENT)
    def request_confirmation(self):
        self.repositories.users.resend_confirmation(user_id=self.user.id)

    @user_router.post("/profile-picture", status_code=status.HTTP_204_NO_CONTENT)
    async def upload_profile_picture(self, file: UploadFile = File(...)):

        if file.content_type not in self.settings.ALLOWED_IMAGE_TYPES:
            raise InventoryHeroAPIException(status_code=status.HTTP_400_BAD_REQUEST, detail=ErrorResponse(
                message=self.localizer.t('user.invalid_profile_picture'),
                toast=True
            ))

        contents: bytes = await file.read()
        image = Image.open(io.BytesIO(contents))


        file_name = f"{str(self.user.id)}.webp"
        file_path = self.settings.PROFILE_PICTURE_DATA_DIR / file_name

        image.save(file_path, format="WEBP", quality=90)

    @user_router.get("/profile-picture")
    async def get_profile_picture(self, response: Response):
        file_name = f"{str(self.user.id)}.webp"
        file_path = self.settings.PROFILE_PICTURE_DATA_DIR / file_name
        if file_path.exists():
            # Set caching headers: cache for 1 day
            cache_duration = timedelta(days=1).total_seconds()
            response.headers["Cache-Control"] = f"public, max-age={int(cache_duration)}"

            return FileResponse(file_path, media_type="image/webp")

        default_url = f"https://api.dicebear.com/8.x/bottts-neutral/svg?seed={str(self.user.id)}"
        async with httpx.AsyncClient() as client:
            resp = await client.get(default_url)
            if resp.status_code != 200:
                raise HTTPException(status_code=502, detail="Default image unavailable")
            return StreamingResponse(io.BytesIO(resp.content), media_type="image/svg+xml")