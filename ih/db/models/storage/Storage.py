from sqlmodel import SQLModel, Field, Relationship
from typing import List, Optional
import uuid
from enum import Enum

class StorageType(str, Enum):
    ROOM = "room"
    BOX = "box"


# Storage Location Table
class Storage(SQLModel, table=True):
    __tablename__ = "storage"

    id: Optional[uuid.UUID] = Field(default_factory=uuid.uuid4, primary_key=True)
    name: str = Field(index=True)
    storage_type: StorageType  = Field()# e.g., "Room", "Box", etc.
    parent_id: Optional[uuid.UUID] = Field(default=None, foreign_key="storage.id")
    household_id: uuid.UUID = Field(foreign_key="household.id", nullable=False, ondelete="CASCADE")
    item_locations: List["ItemStorage"] = Relationship(back_populates="storage")

    parent: Optional["Storage"] = Relationship(
        back_populates="children",
        # sa_relationship_kwargs tells SQLAlchemy how to handle the self-join
        sa_relationship_kwargs=dict(remote_side="Storage.id")
    )
    children: List["Storage"] = Relationship(back_populates="parent")
    household: "Household" = Relationship()

