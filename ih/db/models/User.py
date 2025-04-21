from sqlmodel import SQLModel, Field, Relationship
from typing import Optional
from datetime import datetime

from ih.db.models.RefreshToken import RefreshToken
from ih.db.models.households.HouseholdMember import HouseholdMember


class User(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True, index=True)
    username: str = Field(index=True, unique=True)
    email: str = Field(index=True, unique=True)
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    password: str = Field(nullable=False)
    confirmed: Optional[bool] = False
    confirmation_code: Optional[str] = None
    reset: Optional[bool] = False
    admin: bool = False
    registered_on: datetime = Field(default_factory=lambda: datetime.now())
    household: Optional[int] = Field(default=None, foreign_key="household.id", ondelete="SET NULL")

    refresh_tokens: list[RefreshToken] = Relationship(back_populates="user", cascade_delete=True)
    household_memberships: list[HouseholdMember] = Relationship(back_populates="user")

