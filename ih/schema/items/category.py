from typing import Optional, List
from pydantic import BaseModel, ConfigDict
from uuid import UUID
from .item_attribute import ItemAttributesCreateSchema
from .item_storage import ItemStorageCreateSchema, ItemStorageWithAttributesReadSchema


class CategoryBaseSchema(BaseModel):
    name: str
    model_config = ConfigDict(from_attributes=True)

class CategoryCreateSchema(CategoryBaseSchema):
    pass

class CategoryReadSchema(CategoryBaseSchema):
    id: UUID

    model_config = ConfigDict(from_attributes=True)
