from typing import List

from fastapi import HTTPException
from fastapi_utils.cbv import cbv
from starlette import status

from ih.routes._base.UserApiRouter import UserAPIRouter
from ih.routes._base.UserControllerBase import UserControllerBase
from ih.schema.households.household import HouseholdPublic, HouseholdCreate, HouseholdUpdate, HouseholdWithMemberPublic

router = UserAPIRouter(prefix="/household", tags=["household"])

@cbv(router)
class HouseholdController(UserControllerBase):

    @router.post("/", response_model=HouseholdWithMemberPublic, status_code=status.HTTP_201_CREATED)
    def create_household(self, household: HouseholdCreate):
        created = self.repositories.households.create(household)
        if created is None:
            raise HTTPException(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY)
        return created


    @router.get("/", response_model=List[HouseholdWithMemberPublic], status_code=status.HTTP_200_OK)
    def get_all_households(self):
        return self.repositories.households.all()

    @router.get("/{household_id}", response_model=HouseholdWithMemberPublic, status_code=status.HTTP_200_OK)
    def get_household(self, household_id: int):
        return self.repositories.households.get(household_id)

    @router.delete("/{household_id}", status_code=status.HTTP_204_NO_CONTENT)
    def delete_household(self, household_id: int):
        self.repositories.households.delete(household_id)

    @router.patch("/{household_id}", response_model=HouseholdPublic)
    def update_household(self, household_id: int, household: HouseholdUpdate):
        return self.repositories.households.update(household_id, household)

    @router.post("/{household_id}/transfer-ownership/{user_id}", status_code=status.HTTP_200_OK)
    def transfer_ownership(self, household_id: int, user_id: int):
        self.repositories.households.transfer_ownership(household_id, user_id)