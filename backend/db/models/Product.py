from ...database import db
from datetime import datetime
from dataclasses import dataclass
from sqlalchemy.orm import Mapped


from backend.db.models.StorageContainer import Storage


@dataclass
class Product(db.Model):
    __tablename__ = "products"
    id: int = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name: str = db.Column(db.String(65535), nullable=False)
    household_id: int = db.Column(db.Integer, db.ForeignKey("household.id"), nullable=False)
    starred: bool = db.Column(db.Boolean, nullable=False, default=False)
    creation_date: datetime = db.Column(db.DateTime, default=datetime.utcnow())
    mappings = db.relationship("ProductContainerMapping", back_populates="product", cascade="all, delete-orphan")

    def serialize(self):
        return {
            "id": self.id,
            "name": self.name,
            "household_id": self.household_id,
            "starred": self.starred,
            "creation_date": self.creation_date
        }

    def __hash__(self):
        return hash(self.id)

@dataclass
class ProductContainerMapping(db.Model):
    __tablename__ = "product_container_mapping"
    id: int = db.Column(db.Integer, primary_key=True, autoincrement=True)
    product_id: int = db.Column(db.Integer, db.ForeignKey("products.id"), nullable=False)
    storage_id: int = db.Column(db.Integer, db.ForeignKey("storage.id", ondelete="SET NULL"), nullable=True)
    amount: int = db.Column(db.Integer, nullable=False, default=0)
    updated_at: datetime = db.Column(db.DateTime, default=datetime.utcnow())
    product: Mapped[Product] = db.relationship("Product", back_populates="mappings")
    storage: Mapped[Storage] = db.relationship("Storage", back_populates="product_mappings")

    def serialize(self):
        return {
            "id": self.id,
            "product": self.product,
            "storage": self.storage,
            "amount": self.amount,
            "updated_at": self.updated_at,
        }
