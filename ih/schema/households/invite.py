from datetime import datetime
from uuid import UUID
from pydantic import BaseModel, ConfigDict

class HouseholdInviteBase(BaseModel):
    id: UUID
    created_at: datetime
    expires_at: datetime

class HouseholdInvitePublic(HouseholdInviteBase):
    code: str
    model_config = ConfigDict(from_attributes=True)


class HouseholdInviteWithMeta(HouseholdInviteBase):
    inviter_name: str
    household_name: str

    model_config = ConfigDict(from_attributes=True)