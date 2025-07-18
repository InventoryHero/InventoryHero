from datetime import date
from typing import Optional, List, Annotated
from pydantic import BaseModel, ConfigDict, computed_field, Field
from uuid import UUID
from pydantic_core import PydanticUndefined


from .item_storage import ItemStorageReadSchema



class ItemAttributesBaseSchema(BaseModel):
    expiration_date: Optional[date] = None
    serial_number: Optional[str] = None
    batch_code: Optional[str] = None
    notes: Optional[str] = None


# Schema for creating a new items attribute
class ItemAttributesCreateSchema(ItemAttributesBaseSchema):
    pass


class ItemAttributesUpdateSchema(BaseModel):
    expiration_date: Optional[date] = None
    serial_number: Optional[str] = None
    batch_code: Optional[str] = None
    notes: Optional[str] = None


# Schema for reading a items attribute from the API
class ItemAttributesReadBaseSchema(ItemAttributesBaseSchema):
    id: UUID
    item_id: UUID

    model_config = ConfigDict(from_attributes=True)

class ItemAttributesReadSchema(ItemAttributesReadBaseSchema):
    storage: List[ItemStorageReadSchema]

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

# Schema for reading a items attribute with its parent items details
#class ProductAttributeReadWithProduct(ProductAttributeRead):
#    items: ProductRead