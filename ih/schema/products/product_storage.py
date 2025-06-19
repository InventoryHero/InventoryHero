from datetime import datetime
from typing import Optional, List
from pydantic import BaseModel, Field, ConfigDict
from uuid import UUID



class ProductStorageBase(BaseModel):
    storage_id: UUID
    quantity: int = Field(default=0, ge=0) # Quantity must be greater than 0

# Schema for creating a new product Storage (placing an item in storage)
class ProductStorageCreate(ProductStorageBase):
    pass

# Schema for updating a product Storage, e.g., changing the quantity
class ProductStorageUpdate(BaseModel):
    quantity: Optional[int] = Field(default=None, gt=0)
    # Moving an item would involve changing the storage_id, often handled by a
    # dedicated endpoint rather than a simple PATCH to the Storage entry itself.
    # For example: POST /products/attributes/{attr_id}/move/{storage_id}

# Schema for reading a product Storage from the API
class ProductStorageRead(ProductStorageBase):
    id: UUID
    product_attribute_id: UUID

    model_config = ConfigDict(from_attributes=True)


