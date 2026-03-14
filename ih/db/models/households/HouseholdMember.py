from datetime import datetime
from typing import Optional
from uuid import UUID, uuid4

from sqlalchemy import Column, func, DateTime, UniqueConstraint
from sqlmodel import SQLModel, Field, Relationship

from ih.schema.households.household import Role

class HouseholdMember(SQLModel, table=True):
    id: Optional[UUID] = Field(default_factory=uuid4, primary_key=True, index=True)
    user_id: UUID = Field(foreign_key="user.id", ondelete="CASCADE", nullable=False)
    household_id: UUID = Field(foreign_key="household.id", ondelete="CASCADE", nullable=False)
    role: str = Field(default=Role.MEMBER)
    joined: datetime = Field(
        default_factory=datetime.now,
        sa_column=Column(DateTime, server_default=func.now(), nullable=False)
    )

    household: "Household" = Relationship(back_populates="household_members")
    user: "User" = Relationship(back_populates="household_memberships")

    __table_args__ = (
        UniqueConstraint("household_id", "user_id", name="user_in_household_unique"),
    )