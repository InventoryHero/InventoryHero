from datetime import datetime
from typing import Optional, List
from pydantic import BaseModel, Field, ConfigDict
from uuid import UUID

from ih.db.models import ItemAttributes


class ItemStorageBaseSchema(BaseModel):
    storage_id: UUID
    quantity: int = Field(default=0, ge=0) # Quantity must be greater than 0

# Schema for creating a new items Storage (placing an item in storage)
class ItemStorageCreateSchema(ItemStorageBaseSchema):
    pass

# Schema for updating a items Storage, e.g., changing the quantity
class ItemStorageUpdateSchema(BaseModel):
    quantity: Optional[int] = Field(default=None, gt=0)
    # Moving an item would involve changing the storage_id, often handled by a
    # dedicated endpoint rather than a simple PATCH to the Storage entry itself.
    # For example: POST /items/attributes/{attr_id}/move/{storage_id}

# Schema for reading a items Storage from the API
class ItemStorageReadSchema(ItemStorageBaseSchema):
    id: UUID
    product_attribute_id: UUID
    quantity: int

    model_config = ConfigDict(from_attributes=True)

class ItemStorageWithAttributesReadSchema(ItemStorageReadSchema):
    attributes: ItemAttributes
    model_config = ConfigDict(from_attributes=True)


