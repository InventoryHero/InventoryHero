from functools import cached_property
from typing import Optional

from sqlmodel import Session

from ih.db.models.User import User
from ih.repositories.HouseholdRepository import HouseholdRepository
from ih.repositories.UserRepository import UserRepository


class RepositoryFactory:
    def __init__(self, session: Session, user: Optional[User]=None, household: Optional[int]=None):
        self.session = session
        self.user = user
        self.household = household

    @cached_property
    def users(self) -> UserRepository:
        return UserRepository(self.session, self.user)

    @cached_property
    def households(self) -> HouseholdRepository:
        return HouseholdRepository(self.session, user=self.user, household=self.household)