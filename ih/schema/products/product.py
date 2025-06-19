from typing import Optional

from pydantic import BaseModel, ConfigDict
from uuid import UUID

from .product_attribute import ProductAttributeCreateSchema, ProductAttributeReadSchema
from .product_storage import ProductStorageCreate, ProductStorageRead


class ProductBaseSchema(BaseModel):
    name: str
    description: Optional[str] = None
    category: Optional[str] = None
    household_id: UUID

    model_config = ConfigDict(from_attributes=True)

class ProductSummarySchema(ProductBaseSchema):
    id: UUID
    total_quantity: int

# Schema for creating a new product via the API
class ProductCreateSchema(ProductBaseSchema):
    pass

class ProductUpdateSchema(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None
    category: Optional[str] = None

class ProductReadSchema(ProductBaseSchema):
    id: UUID

class ProductInstanceCreate(BaseModel):
    attributes: Optional[ProductAttributeCreateSchema] = None
    storage: Optional[ProductStorageCreate] = None

class ProductInstanceReadSchema(ProductReadSchema):
    storage: ProductStorageRead
    model_config = ConfigDict(from_attributes=True)