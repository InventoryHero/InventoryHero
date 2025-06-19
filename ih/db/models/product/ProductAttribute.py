from sqlmodel import SQLModel, Field, Relationship
from typing import Optional, List
from uuid import UUID, uuid4
from datetime import datetime
from .Product import Product

class ProductAttribute(SQLModel, table=True):
    id: UUID = Field(default_factory=uuid4, primary_key=True)
    product_id: UUID = Field(foreign_key="product.id", nullable=False, ondelete="CASCADE")

    expiration_date: Optional[datetime] = None
    serial_number: Optional[str] = None
    batch_code: Optional[str] = None
    notes: Optional[str] = None

    product: Product = Relationship(back_populates="attributes")
    storage: List["ProductLocation"] = Relationship(back_populates="attributes")
