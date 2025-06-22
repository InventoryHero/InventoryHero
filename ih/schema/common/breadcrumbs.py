import uuid

from pydantic import BaseModel

from ih.db.models.storage.Storage import StorageType


class BreadcrumbSchema(BaseModel):
    """Represents a single link in the breadcrumb trail."""
    name: str
    type: StorageType
    id: uuid.UUID