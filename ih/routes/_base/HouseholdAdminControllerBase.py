from functools import cached_property

from ih.repositories.factory import RepositoryFactory
from ih.routes._base.HouseholdControllerBase import HouseholdControllerBase


class HouseholdAdminControllerBase(HouseholdControllerBase):

    @cached_property
    def repositories(self):
        return RepositoryFactory(self.session, self.localizer, user=self.user, household=self.household_id)
