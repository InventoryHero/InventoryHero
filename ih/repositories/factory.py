from functools import cached_property
from typing import Optional

from sqlmodel import Session

from ih.db.models.User import User
from ih.repositories.HouseholdRepository import HouseholdRepository
from ih.repositories.StorageRepository import StorageRepository
from ih.repositories.UserRepository import UserRepository
from uuid import UUID

class RepositoryFactory:
    def __init__(self, session: Session, user: Optional[User]=None, household: Optional[UUID]=None):
        self.session = session
        self.user = user
        self.household = household

    @cached_property
    def users(self) -> UserRepository:
        return UserRepository(self.session, self.user)

    @cached_property
    def households(self) -> HouseholdRepository:
        return HouseholdRepository(self.session, user=self.user, household=self.household)

    @cached_property
    def storage(self) -> StorageRepository:
        return StorageRepository(self.session, self.user, self.household)