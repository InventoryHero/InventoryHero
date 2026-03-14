from datetime import datetime
from typing import Optional, List, Annotated
from pydantic import BaseModel, Field, ConfigDict
from uuid import UUID

from pydantic_core import PydanticUndefined

from ih.db.models import ItemAttributes


class ItemStorageBaseSchema(BaseModel):
    storage_id: UUID
    quantity: int = Field(default=0, ge=0) # Quantity must be greater than 0

# Schema for creating a new items Storage (placing an item in storage)
class ItemStorageCreateSchema(ItemStorageBaseSchema):
    pass

# Schema for updating a items Storage, e.g., changing the quantity
class ItemStorageUpdateSchema(BaseModel):
    quantity: Annotated[Optional[int], Field(gt=0)] = None


# Schema for reading a items Storage from the API
class ItemStorageReadSchema(ItemStorageBaseSchema):
    id: UUID
    product_attribute_id: UUID
    quantity: int

    model_config = ConfigDict(from_attributes=True)

class ItemStorageWithAttributesReadSchema(ItemStorageReadSchema):
    attributes: ItemAttributes
    model_config = ConfigDict(from_attributes=True)


