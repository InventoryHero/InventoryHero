# In your Pydantic schema file (e.g., location_schemas.py)
from enum import Enum
from uuid import UUID
from pydantic import BaseModel, ConfigDict
from typing import Optional, Annotated, Union, Literal

from sqlmodel import Field

from ih.db.models.storage.Storage import StorageType

class ContentType(str, Enum):
    ITEMS = "items"
    BOXES = "boxes"


# Base Schema for all storage types
class StorageBaseSchema(BaseModel):
    name: str
    storage_type: StorageType
    parent_id: Optional[UUID] = None
    model_config = ConfigDict(from_attributes=True)

class StorageCreateSchema(StorageBaseSchema):
     pass

class StorageResponseSchema(StorageBaseSchema):
    id: UUID
    parent_id: Optional[UUID] = None
    model_config = ConfigDict(from_attributes=True1)

class RoomResponseSchema(StorageResponseSchema):
    num_boxes: Optional[int] = None
    num_items: Optional[int] = None
    storage_type: Literal[StorageType.ROOM]
    model_config = ConfigDict(from_attributes=True, frozen=True)

class BoxResponseSchema(StorageResponseSchema):
    num_items: Optional[int] = None
    storage_type: Literal[StorageType.BOX]
    parent: Optional[StorageResponseSchema] = None
    model_config = ConfigDict(from_attributes=True, frozen=True)

AnyStorageResponse = Annotated[
    Union[RoomResponseSchema, BoxResponseSchema],
    Field(discriminator="storage_type")
]

