from functools import cached_property

from ih.repositories.factory import RepositoryFactory
from ih.routes._base.UserControllerBase import UserControllerBase
from ih.core.security.get_user import get_household_admin_or_owner, get_household_member
from fastapi import Depends, Path

from ih.schema.households import  Role


class HouseholdControllerBase(UserControllerBase):
    household_id: int = Path(...)
    role: Role|None = Depends(get_household_member)

    @cached_property
    def repositories(self):
        return RepositoryFactory(self.session, user=self.user, household=self.household_id)
