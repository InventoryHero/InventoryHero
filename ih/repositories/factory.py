from functools import cached_property
from typing import Optional

from sqlmodel import Session

from ih.db.models.User import User
from ih.i18n.localizer import Localizer
from ih.repositories.HouseholdRepository import HouseholdRepository
from ih.repositories.ItemRepository import ItemRepository
from ih.repositories.StorageRepository import StorageRepository
from ih.repositories.UserRepository import UserRepository
from uuid import UUID

class RepositoryFactory:
    def __init__(self, session: Session, localizer: Localizer, user: Optional[User]=None, household: Optional[UUID]=None):
        self.session = session
        self.user = user
        self.household = household
        self.localizer = localizer

    @cached_property
    def users(self) -> UserRepository:
        return UserRepository(self.session, self.localizer, self.user)

    @cached_property
    def households(self) -> HouseholdRepository:
        return HouseholdRepository(self.session, self.localizer, user=self.user, household=self.household)

    @cached_property
    def storage(self) -> StorageRepository:
        return StorageRepository(self.session, self.localizer, self.user, self.household)

    @cached_property
    def items(self) -> ItemRepository:
        return ItemRepository(self.session, self.localizer, self.user, self.household)