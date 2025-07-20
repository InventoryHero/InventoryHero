from functools import cached_property

from sqlalchemy.orm import selectinload
from sqlmodel import select
from starlette import status

from ih.core.logging.logger import get_logger
from ih.db.models.User import User
from ih.db.models.households import HouseholdMember
from ih.repositories.factory import RepositoryFactory
from ih.routes._base.ControllerBase import ControllerBase
from ih.core.security.get_user import get_current_user
from fastapi import Depends, HTTPException

from ih.schema.households import HouseholdWithMemberPublic, HouseholdPublic, HouseholdMemberPublic


class UserControllerBase(ControllerBase):
    user: User = Depends(get_current_user)

    @cached_property
    def household(self) -> HouseholdWithMemberPublic | None:
        if self.user.household is None:
            return None
        query = (
            select(HouseholdMember)
            .where(HouseholdMember.user_id == self.user.id, HouseholdMember.household_id == self.user.household)
            .options(selectinload(HouseholdMember.household))
        )
        result = self.session.exec(query).first()
        if result is None:
            self.user.household = None
            #raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="household_not_found")
            return None
        return HouseholdWithMemberPublic(
            **HouseholdPublic.model_validate(result.household).model_dump(),
            member = HouseholdMemberPublic.model_validate(result)
        )

    @cached_property
    def repositories(self):
        return RepositoryFactory(self.session, user=self.user, household=self.user.household)

