from ...database import db
from datetime import datetime
from dataclasses import dataclass
from sqlalchemy.orm import Mapped


from backend.db.models.StorageContainer import Box, Location, box_product_conditions, location_product_conditions, ContainerTypes



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

    storage_id: int = db.Column(db.Integer, nullable=True, default=None)
    storage_type: int = db.Column(db.Integer, nullable=False, default=0)

    amount: int = db.Column(db.Integer, nullable=False, default=0)
    updated_at: datetime = db.Column(db.DateTime, default=datetime.utcnow())

    product = db.relationship("Product", back_populates="mappings")
    box: Mapped[Box] = db.relationship("Box", back_populates="product_mappings", **box_product_conditions)
    location: Mapped[Location] = db.relationship("Location", back_populates="product_mappings", **location_product_conditions)

    def serialize(self):
        return {
            "id": self.id,
            "product_id": self.product_id,
            "storage": self.box if self.storage_type == int(ContainerTypes.Box) else self.location,
            "storage_type": self.storage_type,
            "amount": self.amount,
            "updated_at": self.updated_at,
        }
