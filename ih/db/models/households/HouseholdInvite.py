from typing import Optional
from uuid import UUID, uuid4
from sqlalchemy import UniqueConstraint
from sqlmodel import SQLModel, Field, Relationship
from datetime import datetime, timedelta

class HouseholdInvite(SQLModel, table=True):
    id: Optional[UUID] = Field(default_factory=uuid4, primary_key=True)
    code: str = Field(nullable=False, index=True, unique=True)
    household_id: UUID = Field(foreign_key="household.id", nullable=False, ondelete="CASCADE")
    inviter: UUID = Field(foreign_key="user.id", nullable=True, ondelete="SET NULL")
    created_at: datetime = Field(default_factory=lambda: datetime.now())
    expires_at: datetime = Field(default_factory=lambda: datetime.now() + timedelta(days=7))
    accepted: bool = Field(default=False)

    household: "Household" = Relationship()
    inviter_user: "User" = Relationship()

    @property
    def inviter_name(self) -> str:
        if self.inviter_user:
            return f"{self.inviter_user.username}".strip()
        return "Unknown"

    @property
    def household_name(self) -> str:
        return self.household.name if self.household else "Unknown"

