from typing import Optional

from sqlalchemy import UniqueConstraint
from sqlmodel import SQLModel, Field
from datetime import datetime, timedelta

class HouseholdInvite(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    code: str = Field(nullable=False, index=True, unique=True)
    household_id: int = Field(foreign_key="household.id", nullable=False, ondelete="CASCADE")
    email: str = Field(nullable=False)
    inviter: int = Field(foreign_key="user.id", nullable=True, ondelete="SET NULL")
    created_at: datetime = Field(default_factory=lambda: datetime.now())
    expires_at: datetime = Field(default_factory=lambda: datetime.now() + timedelta(days=7))
    accepted: bool = Field(default=False)

    __table_args__ = (
        UniqueConstraint("household_id", "email", name="unique_invite_per_household_email"),
    )