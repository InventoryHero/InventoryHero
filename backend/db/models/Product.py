from backend.database import db
from datetime import datetime
from dataclasses import dataclass
from sqlalchemy.orm import Mapped

from backend.db.models.StorageContainer import Storage


@dataclass
class Product(db.Model):
    __tablename__ = "products"
    id: int = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name: str = db.Column(db.String(65535), nullable=False)
    household_id: int = db.Column(db.Integer, db.ForeignKey("household.id", ondelete="CASCADE"), nullable=False)
    starred: bool = db.Column(db.Boolean, nullable=False, default=False)
    creation_date: datetime = db.Column(db.DateTime, default=datetime.utcnow())
    mappings = db.relationship("ProductContainerMapping", back_populates="product", cascade="all, delete-orphan")
    household = db.relationship("Household", back_populates="products")

    @property
    def serialize(self):
        return {
            "id": self.id,
            "name": self.name,
            "householdId": self.household_id,
            "starred": self.starred,
            "creationDate": self.creation_date,
            "totalAmount": sum(mapping.amount for mapping in self.mappings)
        }

    def __hash__(self):
        return hash(self.id)


@dataclass
class ProductContainerMapping(db.Model):
    __tablename__ = "product_container_mapping"
    id: int = db.Column(db.Integer, primary_key=True, autoincrement=True)
    product_id: int = db.Column(db.Integer, db.ForeignKey("products.id", ondelete="CASCADE"), nullable=False)
    storage_id: int = db.Column(db.Integer, db.ForeignKey("storage.id", ondelete="SET NULL"), nullable=True)
    amount: int = db.Column(db.Integer, nullable=False, default=0)
    updated_at: datetime = db.Column(db.DateTime, default=datetime.utcnow())
    storage: Mapped[Storage] = db.relationship("Storage", back_populates="product_mappings")
    product = db.relationship("Product", back_populates="mappings")

    @property
    def serialize(self):
        return {
            "id": self.id,
            "productId": self.product_id,
            "storage": self.storage,
            "amount": self.amount,
            "updatedAt": self.updated_at,
        }
