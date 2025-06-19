from datetime import datetime
from typing import Optional, List
from pydantic import BaseModel, ConfigDict, computed_field
from uuid import UUID

from .product_storage import ProductStorageRead


class ProductAttributeBase(BaseModel):
    expiration_date: Optional[datetime] = None
    serial_number: Optional[str] = None
    batch_code: Optional[str] = None
    notes: Optional[str] = None
    model_config = ConfigDict(from_attributes=True)

# Schema for creating a new product attribute
class ProductAttributeCreateSchema(ProductAttributeBase):
    pass

# Schema for updating an existing product attribute
class ProductAttributeUpdateSchema(BaseModel):
    expiration_date: Optional[datetime] = None
    serial_number: Optional[str] = None
    batch_code: Optional[str] = None
    notes: Optional[str] = None

# Schema for reading a product attribute from the API
class ProductAttributeReadSchema(ProductAttributeBase):
    id: UUID
    product_id: UUID
    storage: List[ProductStorageRead]

    @computed_field
    @property
    def total_quantity(self) -> int:
        """
        Calculates the total quantity of this attribute instance by summing the
        quantities from all its storage locations.
        """
        if not self.storage:
            return 0
        return sum(loc.quantity for loc in self.storage)

    model_config = ConfigDict(from_attributes=True)

# Schema for reading a product attribute with its parent product details
#class ProductAttributeReadWithProduct(ProductAttributeRead):
#    product: ProductRead