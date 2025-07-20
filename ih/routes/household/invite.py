from datetime import datetime
from fastapi import HTTPException
from typing import List
from uuid import UUID

from fastapi_utils.cbv import cbv
from sqlmodel import select
from starlette import status

from ih.db.models.households import HouseholdInvite, HouseholdMember
from ih.routes._base.HouseholdAdminControllerBase import HouseholdAdminControllerBase
from ih.routes._base.UserApiRouter import UserAPIRouter
from ih.routes._base.UserControllerBase import UserControllerBase
from ih.schema.households.invite import HouseholdInvitePublic, HouseholdInviteWithMeta

router = UserAPIRouter(prefix="/{household_id}/invite", tags=["household invite"])
accept_invite_router = UserAPIRouter(prefix="/invite", tags=["household invite"])

@cbv(accept_invite_router)
class AcceptInviteController(UserControllerBase):

    def _validate_invite(self, code: str) -> HouseholdInvite:
        invitation = self.repositories.households.get_invitation(code)
        if not invitation or invitation.accepted:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="invite_not_found_or_already_used"
            )

        if invitation.expires_at and invitation.expires_at < datetime.now():
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="invite_expired"
            )

        query = select(HouseholdMember).where(
            HouseholdMember.user_id == self.user.id,
            HouseholdMember.household_id == invitation.household_id
        )
        existing_membership = self.session.exec(query).first()

        if existing_membership:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="user_already_member_of_household"
            )

        return invitation

    @accept_invite_router.get("/validate/{code}", response_model=HouseholdInviteWithMeta, status_code=status.HTTP_202_ACCEPTED)
    def validate_invite(self, code: str):
        print(code)
        invitation = self._validate_invite(code)
        self.logger.warn(HouseholdInviteWithMeta.model_validate(invitation))
        return HouseholdInviteWithMeta.model_validate(invitation)

    @accept_invite_router.post("/accept/{code}", status_code=status.HTTP_200_OK)
    def accept_invite(self, code: str):
        invitation = self._validate_invite(code)
        self.repositories.households.add_member(household_id=invitation.household_id)
        invitation.accepted = True
        self.session.add(invitation)
        self.session.commit()


@cbv(router)
class HouseholdInviteController(HouseholdAdminControllerBase):
    @router.get("/", response_model=List[HouseholdInvitePublic], status_code=status.HTTP_200_OK)
    def get_all(self):
        return self.repositories.households.get_all_invites()


    @router.post("/", response_model=HouseholdInvitePublic, status_code=status.HTTP_200_OK)
    def create_and_send_invite(self):
        invite = self.repositories.households.create_invite()

        if not self.settings.IH_SMTP_ENABLED:
            return invite

        # TODO SEND EMAIL
        return invite

    @router.delete("/{invite_id}", status_code=status.HTTP_204_NO_CONTENT)
    def delete_invite(self, invite_id: UUID):
        self.repositories.households.delete_invite(invite_id)


