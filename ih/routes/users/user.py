from typing import Optional

from fastapi import HTTPException, APIRouter
from fastapi_utils.cbv import cbv
from starlette import status

from uuid import UUID
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
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=self.localizer.t('self_delete_not_possible'))

        success: bool = self.repositories.users.delete(id)
        if not success:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=self.localizer.t('self_delete_not_possible'))

    @admin_router.put("/{user_id}", status_code=200, response_model=UserPublic)
    async def update_user(self, user_id: UUID, to_update: AdminUserUpdate):
        return self.repositories.users.update_user(user_id, to_update)

    @admin_router.put("/{user_id}/reset-password", status_code=status.HTTP_200_OK)
    async def reset_password(self, user_id: UUID):
        return self.repositories.users.request_password_reset_admin(user_id)


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
