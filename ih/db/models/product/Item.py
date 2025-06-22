from sqlmodel import SQLModel, Field, Relationship
from typing import Optional, List
import uuid

from ih.db.models.product.ItemCategoryLink import ItemCategoryLink


class Item(SQLModel, table=True):
    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True)
    household_id: uuid.UUID = Field(foreign_key="household.id", nullable=False)
    name: str
    description: Optional[str] = None
    categories: List["Category"] = Relationship(back_populates="items", link_model=ItemCategoryLink)
    attributes: list["ItemAttributes"] = Relationship(back_populates="item")