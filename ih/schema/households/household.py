from datetime import datetime
from typing import Optional, List

from pydantic import BaseModel, ConfigDict

from ih.schema.user import UserPublic
from enum import Enum

class Role(str, Enum):
    OWNER = "owner"
    ADMIN = "admin"
    MEMBER = "member"

class HouseholdBase(BaseModel):
    name: str

class HouseholdCreate(HouseholdBase):
    pass

class HouseholdPublic(HouseholdBase):
    id: int
    created: datetime
    creator: int
    model_config = ConfigDict(from_attributes=True)

class HouseholdUpdate(HouseholdBase):
    name: Optional[str] = None

class HouseholdSelection(BaseModel):
    id: int


class HouseholdMemberBase(BaseModel):
    id: int
    user_id: int
    joined: datetime
    role: Role

class HouseholdMemberPublic(HouseholdMemberBase):

    user: UserPublic
    model_config = ConfigDict(from_attributes=True)

class HouseholdMemberUpdateRole(BaseModel):
    role: Optional[Role] = None

class HouseholdWithMemberPublic(HouseholdPublic):
    member: HouseholdMemberPublic

class HouseholdWithMembersPublic(HouseholdPublic):
    members: List[HouseholdMemberPublic]

class HouseholdMemberUpdate(HouseholdMemberBase):
    pass
