from time import timezone
from sqlmodel import SQLModel, Field, Relationship, DateTime, String
from sqlalchemy_utc import UtcDateTime
from typing import Optional
from datetime import datetime, timezone
from uuid import UUID, uuid4
from ih.core.security.provider import AuthenticationProvider
from ih.db.models.RefreshToken import RefreshToken
from ih.db.models.households.HouseholdMember import HouseholdMember



class User(SQLModel, table=True):
    id: Optional[UUID] = Field(default_factory=uuid4, primary_key=True, index=True)
    username: str = Field(index=True, unique=True)
    email: str = Field(index=True, unique=True)
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    password: str = Field(nullable=False)
    admin: bool = False
    registered_on: datetime = Field(default_factory=lambda: datetime.now(timezone.utc), sa_type=UtcDateTime)
    household: Optional[UUID] = Field(default=None, foreign_key="household.id", ondelete="SET NULL")

    # email confirmed
    # TODO EXPIRY
    confirmed: Optional[bool] = False
    confirmation_code: Optional[str] = None

    # password reset
    password_reset_token: Optional[str] = None
    password_reset_token_expires_at: Optional[datetime] = Field(
        default=None,
        sa_type=UtcDateTime # <-- And here
    )

    auth_provider: AuthenticationProvider = Field(
        default=AuthenticationProvider.local,
        sa_type=String(length=50),
        nullable=False
    )
    oidc_sub: Optional[str] = Field(default=None, index=True, unique=True, nullable=True)

    reset: Optional[bool] = False


    refresh_tokens: list[RefreshToken] = Relationship(back_populates="user", cascade_delete=True)
    household_memberships: list[HouseholdMember] = Relationship(back_populates="user")

