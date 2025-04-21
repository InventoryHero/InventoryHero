from typing import Sequence, Optional

from fastapi import HTTPException
from sqlalchemy.orm import selectinload
from sqlmodel import Session, select
from starlette import status

from ih.core.security.password import hash_password
from ih.db.models.households import HouseholdMember
from ih.schema.households import HouseholdPublic, HouseholdWithMemberPublic, HouseholdMemberPublic
from ih.schema.user.user import UserPublic, UserCreate, AdminUserCreate
from ih.db.models.User import User



class UserRepository:
    session: Session
    user: Optional[User]
    _household_id: int | None = None

    def __init__(self, session: Session, user: Optional[User]):
        self.session = session
        self.user = user

    @property
    def household_id(self) -> int | None:
        return self._household_id

    def get_all(self) -> Sequence[User]:
        return self.session.exec(select(User)).all()

    def create(self, user: UserCreate | AdminUserCreate) -> User | None:
        query = select(User).where(
            (User.email == user.email) | (User.username == user.username)
        )
        existing_user = self.session.exec(query).first()

        if existing_user is not None:
            reason = "email_already_exists" if user.email == existing_user.email else "username_already_exists"
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail=reason
            )
        admin = getattr(user, "admin", False)
        new_user = User(
            email=user.email,
            username=user.username,
            first_name=user.first_name,
            last_name=user.last_name,
            password=hash_password(user.password),
            admin=admin,
        )

        self.session.add(new_user)
        self.session.commit()
        self.session.refresh(new_user)
        return new_user

    def delete(self, user_id: int) -> bool:
        query = select(User).where(User.id == user_id)
        user = self.session.exec(query).first()
        if user is None:
            return False

        self.session.delete(user)
        self.session.commit()
        return True

    def set_current_household(self, household_id: int) -> HouseholdWithMemberPublic:
        query = (
            select(HouseholdMember)
             .where(HouseholdMember.user_id == self.user.id, HouseholdMember.household_id == household_id)
            .options(selectinload(HouseholdMember.household))
        )
        household = self.session.exec(query).first()
        if household is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="user_is_not_member_of_household"
            )
        self.user.household = household_id
        self.session.add(self.user)
        self.session.commit()
        return HouseholdWithMemberPublic(
            **HouseholdPublic.model_validate(household.household).model_dump(),
            member=HouseholdMemberPublic.model_validate(household)
        )
