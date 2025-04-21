from datetime import datetime

from pydantic import BaseModel, ConfigDict


class HouseholdInviteBase(BaseModel):
    email: str

class HouseholdInviteCreate(HouseholdInviteBase):
    pass


class HouseholdInvitePublic(HouseholdInviteBase):
    id: int
    code: str
    created_at: datetime
    expires_at: datetime
    accepted: bool

    model_config = ConfigDict(from_attributes=True)