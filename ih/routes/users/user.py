from typing import Optional

from fastapi import HTTPException
from fastapi_utils.cbv import cbv
from starlette import status

from ih.schema.households import HouseholdSelection, HouseholdWithMemberPublic
from ih.schema.user.user import UserPublic, AdminUserCreate
from ih.routes._base.AdminApiRouter import AdminAPIRouter
from ih.routes._base.AdminControllerBase import BaseAdminController
from ih.routes._base.UserApiRouter import UserAPIRouter
from ih.routes._base.UserControllerBase import UserControllerBase

user_router = UserAPIRouter(
    prefix="/user",
    tags=["user"],
)

admin_router = AdminAPIRouter(
    prefix="/user",
    tags=["user admin"],
)

@cbv(admin_router)
class AdminUserController(BaseAdminController):
    @admin_router.get("/", response_model=list[UserPublic])
    async def get_all(self):
        return self.repositories.users.get_all()

    @admin_router.post("/create", response_model=UserPublic, status_code=201)
    async def create(self, user: AdminUserCreate):
        return self.repositories.users.create(user)

    @admin_router.delete("/{id}", status_code=204)
    async def delete(self, id: int):
        if id == 0:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="cannot_delete_user_0")

        success: bool = self.repositories.users.delete(id)
        if not success:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="cannot_delete_user_0")


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