# In your Pydantic schema file (e.g., location_schemas.py)

from uuid import UUID
from pydantic import BaseModel, ConfigDict
from typing import Optional
from ih.db.models.storage.Storage import StorageType  # Import StorageType Enum

# Base Schema for all storage types
class StorageBaseSchema(BaseModel):
    name: str
    parent_id: Optional[UUID] = None
    model_config = ConfigDict(from_attributes=True)

# Location Specific Schema
class RoomCreateSchema(StorageBaseSchema):
    storage_type: StorageType = StorageType.ROOM  # Default to room type for location

# Box Specific Schema
class BoxCreateSchema(StorageBaseSchema):
    storage_type: StorageType = StorageType.BOX  # Default to box type for box

# Response Schema
class StorageResponseSchema(StorageBaseSchema):
    id: UUID
    storage_type: StorageType
    household_id: UUID

    model_config = ConfigDict(from_attributes=True)
