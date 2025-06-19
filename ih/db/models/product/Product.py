from sqlmodel import SQLModel, Field, Relationship
from typing import Optional
import uuid


class Product(SQLModel, table=True):
    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True)
    household_id: uuid.UUID = Field(foreign_key="household.id", nullable=False)
    name: str
    description: Optional[str] = None
    category: Optional[str] = None

    attributes: list["ProductAttribute"] = Relationship(back_populates="product")