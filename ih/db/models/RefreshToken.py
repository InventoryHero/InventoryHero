from datetime import datetime
from typing import Optional
from uuid import UUID

from sqlmodel import SQLModel, Field, Relationship


class RefreshToken(SQLModel, table=True):
    jti: str = Field(primary_key=True)
    user_id: UUID = Field(foreign_key="user.id", ondelete="CASCADE")
    created_at: datetime =  Field(default_factory=lambda: datetime.now())
    revoked: bool = False
    expires_at: datetime

    user: Optional["User"] = Relationship(back_populates="refresh_tokens")