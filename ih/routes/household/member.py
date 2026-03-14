from fastapi import HTTPException
from fastapi_utils.cbv import cbv
from starlette import status
from uuid import UUID

from ih.routes._base.HouseholdControllerBase import HouseholdControllerBase
from ih.routes._base.UserApiRouter import UserAPIRouter
from ih.routes._base.HouseholdAdminControllerBase import HouseholdAdminControllerBase
from ih.schema.households import HouseholdWithMembersPublic, HouseholdMemberUpdateRole, Role

router = UserAPIRouter(prefix="/{household_id}/member", tags=["household member"])


@cbv(router)
class HouseholdController(HouseholdAdminControllerBase):

    @router.get("/", response_model=HouseholdWithMembersPublic, status_code=status.HTTP_200_OK)
    def get_all_member(self):
        return self.repositories.households.get_all_members(self.household_id)

    @router.delete("/{member_id}", status_code=status.HTTP_204_NO_CONTENT)
    def remove_member(self, household_id: UUID, member_id: UUID):
        self.repositories.households.remove_member(household_id, member_id)

    @router.patch("/{member_id}", status_code=status.HTTP_200_OK)
    def update_member_role(self, household_id: UUID, member_id: UUID, update: HouseholdMemberUpdateRole):
        if update.role not in [Role.ADMIN, Role.MEMBER]:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST
            )
        self.repositories.households.update_member_role(household_id, member_id, update)

@cbv(router)
class HouseholdController(HouseholdControllerBase):
    @router.delete("/", status_code=status.HTTP_204_NO_CONTENT)
    def leave_household(self):
        self.repositories.households.leave_household()


