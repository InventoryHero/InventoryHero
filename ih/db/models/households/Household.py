from datetime import datetime
from typing import Optional

from sqlmodel import SQLModel, Field, Relationship

from ih.db.models.households.HouseholdMember import HouseholdMember


class Household(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True, index=True)
    name: str = Field(index=True)
    created: datetime = Field(default_factory=lambda: datetime.now())
    creator: int = Field(foreign_key="user.id", nullable=False)

    household_members: list[HouseholdMember] = Relationship(back_populates="household", cascade_delete=True)