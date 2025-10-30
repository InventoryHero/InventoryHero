from functools import cached_property

from fastapi import Depends

from ih.core.security.get_user import get_admin_user
from ih.db.models import User
from ih.repositories.factory import RepositoryFactory
from ih.routes._base.UserControllerBase import UserControllerBase


class BaseAdminController(UserControllerBase):
    user: User = Depends(get_admin_user)

    @cached_property
    def repositories(self):
        return RepositoryFactory(self.session, self.localizer, user=self.user)
