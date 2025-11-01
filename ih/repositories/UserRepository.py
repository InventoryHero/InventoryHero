import hashlib
import secrets
from datetime import datetime, timedelta, UTC, timezone

from ih.core.exceptions.exceptions import InventoryHeroAPIException
from ih.schema.common.error_response import ErrorResponse
from typing import Sequence, Optional
from uuid import UUID
from fastapi import HTTPException

from sqlalchemy.orm import selectinload
from sqlmodel import Session, select
from starlette import status
import logging

from ih.core.config import get_app_settings
from ih.core.logging.logger import get_logger
from ih.core.security.password import hash_password, verify_password
from ih.db.models.households import HouseholdMember
from ih.i18n.localizer import Localizer
from ih.schema.households import HouseholdPublic, HouseholdWithMemberPublic, HouseholdMemberPublic
from ih.schema.user.user import UserPublic, UserCreate, AdminUserCreate, UserUpdate, UserCreateBase, \
    ChangePasswordFormBase, AdminUserUpdate
from ih.db.models.User import User
from ih.services.email.email import send_confirmation_email, send_password_reset_email


class UserRepository:
    session: Session
    user: Optional[User]
    _household_id: UUID | None = None
    _logger: logging.Logger = get_logger()

    def __init__(self, session: Session, localizer: Localizer, user: Optional[User]):
        self.session = session
        self.user = user
        self.localizer = localizer

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
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=self.localizer.t("user_not_found"))

        return user

    def create_user_admin(self, user: AdminUserCreate):
        return self.create(user, user.admin)

    def register(self, user: UserCreate):
        if user.password != user.password_confirmation:
            raise HTTPException(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
                                detail=self.localizer.t("passwords_dont_match"))
        self.create(user, False)

    def create(self, user: UserCreateBase, is_admin: bool = False) -> User | None:

        settings = get_app_settings()

        query = select(User).where(
            (User.email == user.email) | (User.username == user.username)
        )
        existing_user = self.session.exec(query).first()

        if existing_user is not None:
            reason = "email_already_exists" if user.email == existing_user.email else "username_already_exists"
            raise InventoryHeroAPIException(
                status_code=status.HTTP_409_CONFLICT,
                detail=ErrorResponse(
                    message=reason,
                    toast=False
                )
            )

        confirmation_code = None
        confirmation_hash = None
        if settings.IH_SMTP_ENABLED:
            confirmation_code = secrets.token_urlsafe(32)
            confirmation_hash = hashlib.sha256(confirmation_code.encode()).hexdigest()

        new_user = User(
            email=user.email,
            username=user.username,
            first_name=user.first_name,
            last_name=user.last_name,
            password=hash_password(user.password),
            admin=is_admin,
            confirmed=not settings.IH_SMTP_ENABLED,
            confirmation_code=confirmation_hash
        )

        self.session.add(new_user)
        self.session.flush()
        self.session.refresh(new_user)

        self._logger.info(f"User: {new_user.username} successfully created")
        send_confirmation_email(user.email, user.username, confirmation_code)
        return new_user

    def delete(self, user_id: UUID) -> bool:
        query = select(User).where(User.id == user_id)
        user = self.session.exec(query).first()
        if user is None:
            return False

        if user.admin:
            other_admins = self.session.exec(query.where(User.id != user_id, User.admin)).first()
            if other_admins is None:
                raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=self.localizer.t("last_admin"))

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
                detail=self.localizer.t("user_is_not_member_of_household")
            )
        self.user.household = household_id
        self.session.add(self.user)
        self.session.commit()
        return HouseholdWithMemberPublic(
            **HouseholdPublic.model_validate(household.household).model_dump(),
            member=HouseholdMemberPublic.model_validate(household)
        )

    def update_user_admin(self, user_id: UUID, to_update: AdminUserUpdate) -> UserPublic:
        update_data = to_update.model_dump(exclude_unset=True)
        user_fields = {k: v for k, v in update_data.items() if k in UserUpdate.model_fields}
        admin_fields = {k: v for k, v in update_data.items() if k not in UserUpdate.model_fields}
        user = self.update_user(user_id, UserUpdate(**user_fields))
        for field, value in admin_fields.items():
            setattr(user, field, value)
        self.session.flush()
        self.session.refresh(user)
        return user

    def update_user(self, user_id: UUID, to_update: UserUpdate) -> UserPublic:
        settings = get_app_settings()
        update_data = to_update.model_dump(exclude_unset=True)
        user = self.get_user_by_id(user_id)
        if not update_data:
            return user

        reconfirm_email = False

        for field, value in update_data.items():
            if field == "email" and settings.IH_SMTP_ENABLED:
                reconfirm_email = True
                setattr(user, 'confirmed', False)
            setattr(user, field, value)
        self.session.flush()
        self.session.refresh(user)
        if reconfirm_email:
            self.resend_confirmation(user_id=user_id)
        return user

    def change_password(self, user_id: UUID, current_password: str, new_password: str,
                        new_password_confirmation: str) -> None:
        if new_password != new_password_confirmation:
            raise InventoryHeroAPIException(
                status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
                detail=ErrorResponse(
                    message=self.localizer.t("password_reset.password_mismatch")
                )
            )
        user = self.get_user_by_id(user_id)
        if not verify_password(current_password, user.password):
            raise InventoryHeroAPIException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail=ErrorResponse(
                    message="wrong_password",
                    toast=False
                )
            )

        user.password = hash_password(new_password)
        self.session.flush()

    def confirm_email(self, code: str) -> None:
        confirmation_hash = hashlib.sha256(code.encode()).hexdigest()
        user = self.session.exec(
            select(User)
            .where(User.confirmation_code == confirmation_hash)
        ).first()

        if user is None:
            raise InventoryHeroAPIException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=ErrorResponse(
                    message=self.localizer.t("email_confirmation.code_not_found"),
                    toast=False
                )
            )

        user.confirmed = True
        user.confirmation_code = None
        self.session.flush()

    def request_password_reset_admin(self, user_id: UUID, requestee: str) -> str:
        user = self.session.exec(select(User).where(User.id == user_id)).first()
        if user is None:
            raise InventoryHeroAPIException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=ErrorResponse(
                    message=self.localizer.t("user_not_found"),
                    toast=True
                )
            )
        code = self.generate_password_reset_code(user, requestee)
        return code

    def request_password_reset(self, email: str) -> None:
        user = self.session.exec(select(User).where(User.email == email)).first()
        if user is None:
            return
        _ =  self.generate_password_reset_code(user, None)

    def generate_password_reset_code(self, user: User, admin: Optional[str] = None) -> str:
        password_reset_code = secrets.token_urlsafe(32)
        password_reset_token = hashlib.sha256(password_reset_code.encode()).hexdigest()

        user.password_reset_token = password_reset_token
        user.password_reset_token_expires_at = datetime.now(timezone.utc) + timedelta(minutes=60)
        settings = get_app_settings()

        self.session.flush()
        reset_url = f"{settings.IH_APP_URL}/password-reset/{password_reset_code}"

        send_password_reset_email(to=user.email, username=user.username, reset_url=reset_url, admin_username=admin)
        return reset_url
        # print(password_reset_code)
        # TODO SEND EMAIL

    def validate_password_token(self, code: str) -> bool:
        password_token = hashlib.sha256(code.encode()).hexdigest()
        user = self.session.exec(
            select(User)
            .where(User.password_reset_token == password_token)
        ).first()

        if user is None:
            return False

        if datetime.now(timezone.utc) > user.password_reset_token_expires_at:
            return False

        return True

    def reset_password(self, code: str, new_password: ChangePasswordFormBase) -> (bool, str):
        password_token = hashlib.sha256(code.encode()).hexdigest()
        user = self.session.exec(
            select(User)
            .where(User.password_reset_token == password_token)
        ).first()

        if user is None:
            return False, ''

        if datetime.now(timezone.utc) > user.password_reset_token_expires_at:
            return False, self.localizer.t('password_reset.invalid_token')

        if new_password.new_password != new_password.new_password_confirmation:
            raise InventoryHeroAPIException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=ErrorResponse(
                    message=self.localizer.t('password_reset.passwords_dont_match'),
                    toast=True
                )
            )

        user.password = hash_password(new_password.new_password)
        self.session.flush()
        return True, ''

    def resend_confirmation(self, user_id: UUID) -> None:

        settings = get_app_settings()
        if not settings.IH_SMTP_ENABLED:
            raise InventoryHeroAPIException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=ErrorResponse(
                    message=self.localizer.t("email_confirmation.smtp_disabled")
                )
            )

        query = select(User).where(User.id == user_id)

        user = self.session.exec(query).first()
        if user is None:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                                detail=self.localizer.t('email_confirmation.user_not_found'))

        confirmation_code = secrets.token_urlsafe(32)
        confirmation_hash = hashlib.sha256(confirmation_code.encode()).hexdigest()

        user.confirmation_code = confirmation_hash

        self._logger.info(f"Resent confirmation e-mail to {user.email}")
        send_confirmation_email(user.email, user.username, confirmation_code)
        self.session.flush()


