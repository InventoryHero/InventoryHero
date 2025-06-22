from typing import Optional, List, Dict, Set
from pydantic import BaseModel, ConfigDict
from uuid import UUID
from .item_attribute import ItemAttributesCreateSchema, ItemAttributesReadBaseSchema
from .item_storage import ItemStorageCreateSchema, ItemStorageWithAttributesReadSchema, ItemStorageReadSchema
from .category import CategoryReadSchema
from ..common import BreadcrumbSchema
from ..storage import StorageResponseSchema


class ItemBaseSchema(BaseModel):
    name: str
    description: Optional[str] = None


    model_config = ConfigDict(from_attributes=True)

class ItemSummarySchema(ItemBaseSchema):
    id: UUID
    total_quantity: int
    categories: Optional[List["CategoryReadSchema"]] = None

# Schema for creating a new items via the API
class ItemCreateSchema(ItemBaseSchema):
    categories: List[UUID] = []
    pass

class ProductUpdateSchema(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None
    categories_to_add: Optional[List[UUID]]
    categories_to_remove: Optional[List[UUID]]

class ItemReadSchema(ItemBaseSchema):
    id: UUID
    categories: List["CategoryReadSchema"]

class ItemDetailReadSchema(ItemReadSchema):
    items: Dict[UUID, List[ItemStorageReadSchema]]
    storage: List[StorageResponseSchema]
    attributes: Dict[UUID, ItemAttributesReadBaseSchema]
    breadcrumbs: Optional[List[BreadcrumbSchema]] = []

class ItemInstanceCreate(BaseModel):
    attributes: Optional[ItemAttributesCreateSchema] = None
    storage: Optional[ItemStorageCreateSchema] = None

class ItemInstanceReadSchema(ItemReadSchema):
    storage: ItemStorageWithAttributesReadSchema
    model_config = ConfigDict(from_attributes=True)
