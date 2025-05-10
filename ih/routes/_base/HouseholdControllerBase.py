from functools import cached_property
from uuid import UUID
from ih.repositories.factory import RepositoryFactory
from ih.routes._base.UserControllerBase import UserControllerBase
from ih.core.security.get_user import get_household_member, get_household_id
from fastapi import Depends, Path

from ih.schema.households import  Role


class HouseholdControllerBase(UserControllerBase):
    household_id: UUID = Depends(get_household_id)
    role: Role|None = Depends(get_household_member)

    @cached_property
    def repositories(self):
        return RepositoryFactory(self.session, user=self.user, household=self.household_id)
