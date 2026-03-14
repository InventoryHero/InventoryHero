from datetime import datetime
from typing import Optional, List
from uuid import UUID

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
    id: UUID
    created: datetime
    #creator: int
    model_config = ConfigDict(from_attributes=True)

class HouseholdUpdate(HouseholdBase):
    name: Optional[str] = None

class HouseholdSelection(BaseModel):
    id: UUID


class HouseholdMemberBase(BaseModel):
    id: UUID
    user_id: UUID
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
