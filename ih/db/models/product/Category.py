# In a new file, e.g., db/models/category.py
from sqlmodel import SQLModel, Field, Relationship
from typing import List, Optional
from uuid import UUID, uuid4

from ih.db.models.product.ItemCategoryLink import ItemCategoryLink


class Category(SQLModel, table=True):
    id: UUID = Field(default_factory=uuid4, primary_key=True)
    household_id: UUID = Field(foreign_key="household.id", nullable=False)
    name: str = Field(index=True)
    color: Optional[str] = None # e.g., "#4A90E2" for the pill background
    icon_name: Optional[str] = None # e.g., "bi-box" from our icon discussion

    # The list of products that have this category
    items: List["Item"] = Relationship(back_populates="categories", link_model=ItemCategoryLink)