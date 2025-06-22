from uuid import UUID

from sqlmodel import SQLModel, Field


class ItemCategoryLink(SQLModel, table=True):
    item_id: UUID = Field(foreign_key="item.id", primary_key=True)
    category_id: UUID = Field(foreign_key="category.id", primary_key=True)