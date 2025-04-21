from fastapi import Depends

from ih.core.security.get_user import try_get_current_user
from ih.db.models.User import User
from ih.routes._base.ControllerBase import ControllerBase


class PublicControllerBase(ControllerBase):
    user: User | None = Depends(try_get_current_user)