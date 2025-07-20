import hashlib
import secrets
from typing import Optional, List, Union
from uuid import UUID

from fastapi import HTTPException
from sqlalchemy import delete
from sqlalchemy.exc import IntegrityError

from sqlalchemy.orm import selectinload
from sqlmodel import Session, select
from starlette import status

from ih.db.models.User import User
from ih.db.models.households import Household, HouseholdMember, HouseholdInvite
from ih.schema.households.household import HouseholdCreate, HouseholdPublic, HouseholdUpdate, \
    HouseholdWithMembersPublic, HouseholdMemberPublic, HouseholdWithMemberPublic, Role, HouseholdMemberUpdateRole
from ih.schema.households.invite import HouseholdInvitePublic


class HouseholdRepository:
    session: Session
    user: Optional[User]
    household_id: Optional[UUID]

    def __init__(self, session: Session, user: Optional[User] = None, household: Optional[UUID] = None):
        self.session = session
        self.user = user
        self.household_id = household

    def _get_household(self, household_id: UUID) -> Household:
        query = select(Household).where(Household.id == household_id)
        household = self.session.exec(query).first()

        if household is None:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="household_not_found")
        return household


    def _get_member(self, household_id: UUID,
                    user_id: UUID = None,
                    include_user: bool = False,
                    include_household: bool = False) -> Union[HouseholdMember, List[HouseholdMember]]:
        base_query = (
            select(HouseholdMember)
            .where(HouseholdMember.household_id == household_id)
        )

        if include_user:
            base_query = base_query.options(selectinload(HouseholdMember.user))

        if include_household:
            base_query = base_query.options(selectinload(HouseholdMember.household))
        requester_query = base_query.where(HouseholdMember.user_id == self.user.id)
        requester = self.session.exec(requester_query).first()

        if requester is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="not_found"
            )

        if requester.role not in [Role.ADMIN, Role.OWNER]:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="no_rights"
            )

        if user_id is None:
            return self.session.exec(base_query).all()
        elif user_id == self.user.id:
            return requester

        user_query = base_query.where(HouseholdMember.user_id == user_id)
        user = self.session.exec(user_query).first()
        if user is None:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="user_not_in_household")
        return user

    def create(self, household: HouseholdCreate):
        household = Household(
            name = household.name,
            creator = self.user.id,
        )
        self.session.add(household)
        self.session.commit()
        self.session.refresh(household)
        member = HouseholdMember(
            household_id = household.id,
            user_id = self.user.id,
            role = "owner"
        )

        self.session.add(member)
        self.session.commit()
        self.session.refresh(member)
        self.session.refresh(household)
        return HouseholdWithMemberPublic(
            **HouseholdPublic.model_validate(household).model_dump(),
            member = HouseholdMemberPublic.model_validate(member)
        )

    def get(self, household_id: UUID) -> HouseholdWithMembersPublic:
        member = self._get_member(household_id, user_id=None, include_household=True)
        return HouseholdWithMembersPublic(
            **HouseholdPublic.model_validate(member.household).model_dump(),
            members = [HouseholdMemberPublic.model_validate(member)]
        )

    def all(self) -> list[HouseholdWithMemberPublic]:
        query = (
            select(HouseholdMember)
            .where(HouseholdMember.user_id == self.user.id)
            .options(selectinload(HouseholdMember.household))
        )
        results = self.session.exec(query).all()
        if not results:
            return []

        return [
            HouseholdWithMemberPublic(
                **HouseholdPublic.model_validate(household_member.household).model_dump(),
                member = HouseholdMemberPublic.model_validate(household_member)
            ) for household_member in results
        ]

    def delete(self, household_id: UUID):
        household_member = self._get_member(household_id, user_id=self.user.id, include_household=True)
        self.session.delete(household_member.household)
        self.session.commit()

    def update(self, household_id: UUID, update_data: HouseholdUpdate) -> HouseholdPublic:
        household_member = self._get_member(household_id, user_id=self.user.id, include_household=True)

        household_data_dict = update_data.model_dump(exclude_unset=True)
        for key, value in household_data_dict.items():
            setattr(household_member.household, key, value)

        self.session.add(household_member.household)
        self.session.commit()
        self.session.refresh(household_member.household)
        return household_member.household


    def get_all_members(self, household_id: UUID) -> HouseholdWithMembersPublic:
        results = self._get_member(household_id, user_id=None, include_user=True)
        if not results:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)

        household = self._get_household(household_id)
        return HouseholdWithMembersPublic(
            **HouseholdPublic.model_validate(household).model_dump(),
            members = [HouseholdMemberPublic.model_validate(member) for member in results]
        )

    def transfer_ownership(self, household_id: UUID, user_id: UUID):
        curr_owner = self._get_member(household_id, self.user.id)
        if curr_owner.role != Role.OWNER:
            raise HTTPException(status_code=403, detail="only_owner_can_transfer_ownership")
        if user_id == self.user.id:
            raise HTTPException(status_code=400, detail="already_owner")

        new_owner = self._get_member(household_id, user_id=user_id, include_user=True)

        curr_owner.role = Role.ADMIN # Downgrade current owner to admin
        new_owner.role = Role.OWNER

        self.session.add(new_owner)
        self.session.add(curr_owner)
        self.session.commit()

    def remove_member(self, household_id: UUID, member_id: UUID):
        to_remove = self._get_member(household_id, user_id=member_id, include_user=True)
        if to_remove.role == Role.OWNER:
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="cannot_remove_owner")

        if to_remove.user.household == to_remove.household_id:
            to_remove.user.household = None
            self.session.add(to_remove.user)

        self.session.delete(to_remove)
        self.session.commit()

    def leave_household(self):
        query = select(HouseholdMember).where(HouseholdMember.user_id == self.user.id, HouseholdMember.household_id == self.household_id)
        to_remove = self.session.exec(query).first()
        if not to_remove:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="user_is_not_member_of_household")
        if to_remove.role == Role.OWNER:
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="cannot_remove_owner")
        self.session.delete(to_remove)
        self.session.commit()


    def update_member_role(self, household_id: UUID, member_id: UUID,  update: HouseholdMemberUpdateRole):
        to_update = self._get_member(household_id, user_id=member_id, include_user=True)
        if to_update.role == Role.OWNER:
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="cannot_update_owner")

        to_update.role = update.role
        self.session.add(to_update)
        self.session.commit()

    def create_invite(self )-> HouseholdInvitePublic:

        raw_code = secrets.token_urlsafe(32)
        code_hash = hashlib.sha256(raw_code.encode()).hexdigest()
        invite = HouseholdInvite(code=code_hash, household_id=self.household_id, inviter=self.user.id)
        try:
            self.session.add(invite)
            self.session.commit()
            self.session.refresh(invite)

        except IntegrityError:
            self.session.rollback()
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="invite_email_household_exists"
            )

        public_invite = HouseholdInvitePublic(**invite.model_dump(exclude={"code"}), code=raw_code)
        return public_invite

    def delete_invite(self, invite_id: UUID):
        query = delete(HouseholdInvite).where(HouseholdInvite.id == invite_id, HouseholdInvite.household_id == self.household_id)
        result = self.session.exec(query)
        self.session.commit()

        if result.rowcount == 0:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="invite_not_found"
            )

    def get_all_invites(self):
        query = select(HouseholdInvite).where(HouseholdInvite.household_id == self.household_id)
        invites = self.session.exec(query).all()
        return invites

    def get_invitation(self, code: str) -> HouseholdInvite | None:
        code = hashlib.sha256(code.encode()).hexdigest()
        query = select(HouseholdInvite).where(HouseholdInvite.code == code).options(
            selectinload(HouseholdInvite.household),
            selectinload(HouseholdInvite.inviter_user)
        )
        return self.session.exec(query).first()

    def add_member(self, household_id: UUID):
        new_member = HouseholdMember(
            household_id=household_id,
            user_id=self.user.id
        )
        self.session.add(new_member)
        self.session.commit()


