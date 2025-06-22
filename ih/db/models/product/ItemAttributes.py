from sqlmodel import SQLModel, Field, Relationship
from typing import Optional, List
from uuid import UUID, uuid4
from datetime import datetime
from .Item import Item

class ItemAttributes(SQLModel, table=True):
    id: UUID = Field(default_factory=uuid4, primary_key=True)
    item_id: UUID = Field(foreign_key="item.id", nullable=False, ondelete="CASCADE")

    expiration_date: Optional[datetime] = None
    serial_number: Optional[str] = None
    batch_code: Optional[str] = None
    notes: Optional[str] = None

    item: Item = Relationship(back_populates="attributes")
    storage: List["ItemStorage"] = Relationship(back_populates="attributes")
