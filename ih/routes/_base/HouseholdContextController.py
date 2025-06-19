from functools import cached_property

from fastapi import HTTPException
from starlette import status

from ih.repositories.factory import RepositoryFactory
from ih.routes._base.UserControllerBase import UserControllerBase
from ih.schema.households import HouseholdWithMemberPublic


class HouseholdContextController(UserControllerBase):
    @cached_property
    def household(self) -> HouseholdWithMemberPublic:
        base_household = super().household
        if base_household is None:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="no_household_set"
            )
        return base_household

    @cached_property
    def repositories(self):
        return RepositoryFactory(self.session, user=self.user, household=self.household.id)