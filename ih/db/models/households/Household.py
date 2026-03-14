from datetime import datetime
from typing import Optional
from uuid import UUID, uuid4

from sqlmodel import SQLModel, Field, Relationship

from ih.db.models.households.HouseholdMember import HouseholdMember
from ih.db.models.storage import Storage


class Household(SQLModel, table=True):
    id: Optional[UUID] = Field(default_factory=uuid4, primary_key=True, index=True)
    name: str = Field(index=True)
    created: datetime = Field(default_factory=lambda: datetime.now())
    #creator: UUID = Field(foreign_key="user.id", nullable=False)

    household_members: list[HouseholdMember] = Relationship(back_populates="household", cascade_delete=True)
    storage: list[Storage] = Relationship(back_populates="household", cascade_delete=True)