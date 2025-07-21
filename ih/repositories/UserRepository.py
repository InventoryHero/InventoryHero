import hashlib
import secrets
from typing import Sequence, Optional
from uuid import UUID
from fastapi import HTTPException
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import selectinload
from sqlmodel import Session, select
from starlette import status

from ih.core.security.password import hash_password, verify_password
from ih.db.models.households import HouseholdMember
from ih.schema.households import HouseholdPublic, HouseholdWithMemberPublic, HouseholdMemberPublic
from ih.schema.user.user import UserPublic, UserCreate, AdminUserCreate, UserUpdate, UserCreateBase
from ih.db.models.User import User



class UserRepository:
    session: Session
    user: Optional[User]
    _household_id: UUID | None = None

    def __init__(self, session: Session, user: Optional[User]):
        self.session = session
        self.user = user

    @property
    def household_id(self) -> UUID | None:
        return self._household_id

    def get_all(self) -> Sequence[User]:
        return self.session.exec(select(User)).all()

    def get_user_by_id(self, user_id: UUID):
        result = self.session.exec(
            select(User).where(User.id == user_id)
        )
        user = result.first()

        if not user:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")

        return user

    def create_user_admin(self, user: AdminUserCreate):
        return self.create(user, False, user.admin)

    def register(self, user: UserCreate, need_confirmation: bool = False):
        if user.password != user.password_confirmation:
            raise HTTPException(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY, detail="passwords_dont_match")
        self.create(user, need_confirmation, False)

    def create(self, user: UserCreateBase, confirmation_needed: bool = False, is_admin: bool = False) -> User | None:
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

        confirmation_code = None
        confirmation_hash = None
        if confirmation_needed:
            confirmation_code = secrets.token_urlsafe(32)
            confirmation_hash = hashlib.sha256(confirmation_code.encode()).hexdigest()

        # TODO SEND EMAIL
        print(confirmation_code)

        new_user = User(
            email=user.email,
            username=user.username,
            first_name=user.first_name,
            last_name=user.last_name,
            password=hash_password(user.password),
            admin=is_admin,
            confirmed=not confirmation_needed,
            confirmation_code=confirmation_hash
        )

        self.session.add(new_user)
        self.session.flush()
        self.session.refresh(new_user)
        return new_user

    def delete(self, user_id: UUID) -> bool:
        query = select(User).where(User.id == user_id)
        user = self.session.exec(query).first()
        if user is None:
            return False

        self.session.delete(user)
        self.session.commit()
        return True

    def set_current_household(self, household_id: UUID) -> HouseholdWithMemberPublic:
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

    def update_user(self, user_id: UUID, to_update: UserUpdate) -> UserPublic:
        update_data = to_update.model_dump(exclude_unset=True)
        user = self.get_user_by_id(user_id)
        if not update_data:
            return user
        for field, value in update_data.items():
            setattr(user, field, value)
        self.session.flush()
        self.session.refresh(user)
        return user

    def change_password(self, user_id: UUID, current_password: str, new_password: str, new_password_confirmation: str) -> None:
        if new_password != new_password_confirmation:
            raise HTTPException(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY, detail="passwords_dont_match")
        user = self.get_user_by_id(user_id)
        if not verify_password(current_password, user.password):
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN)

        user.password = hash_password(new_password)
        self.session.flush()

    def confirm_email(self, code: str) -> None:
        confirmation_hash = hashlib.sha256(code.encode()).hexdigest()
        user = self.session.exec(
            select(User)
                .where(User.confirmation_code == confirmation_hash)
        ).first()

        if user is None:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="user_not_found")

        user.confirmed = True
        user.confirmation_code = None
        self.session.flush()
