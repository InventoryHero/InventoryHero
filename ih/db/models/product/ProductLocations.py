from sqlmodel import SQLModel, Field, Relationship
from uuid import UUID, uuid4
from .ProductAttribute import ProductAttribute
from ih.db.models.storage import Storage

class ProductLocation(SQLModel, table=True):
    id: UUID = Field(default_factory=uuid4, primary_key=True)
    product_attribute_id: UUID = Field(foreign_key="productattribute.id", nullable=False, ondelete="CASCADE")
    storage_id: UUID = Field(foreign_key="storage.id", nullable=False, ondelete="CASCADE")

    quantity: int = Field(default=0)

    attributes: ProductAttribute = Relationship(back_populates="storage")
    storage: Storage = Relationship()
