from database import db
from enum import Enum
from dataclasses import dataclass
from sqlalchemy.orm import Mapped
from datetime import datetime
import sys


class ContainerTypes(Enum):
    NoContainer = 0
    Box = 1
    Location = 2

    def __int__(self):
        return self.value

box_product_conditions = dict(primaryjoin="and_(Box.id == orm.foreign(ProductContainerMapping.storage_id), Box.type == orm.foreign(ProductContainerMapping.storage_type))", overlaps='product_mappings, location')

location_product_conditions = dict(primaryjoin="and_(Location.id == orm.foreign(ProductContainerMapping.storage_id), Location.type == orm.foreign(ProductContainerMapping.storage_type))", overlaps='product_mappings, box')


@dataclass
class Location(db.Model):
    __tablename__ = "location"
    id: int = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name: str = db.Column(db.String(65535), nullable=False)
    household_id: int = db.Column(db.Integer, db.ForeignKey("household.id"), nullable=False)
    creation_date: datetime = db.Column(db.DateTime, default=datetime.utcnow())
    type: int = db.Column(db.Integer, default=int(ContainerTypes.Location))

    boxes = db.relationship("Box", back_populates="location")
    product_mappings = db.relationship("ProductContainerMapping", back_populates="location", **location_product_conditions)

    def serialize(self):
        return {
            "id": self.id,
            "name": self.name,
            "household_id": self.household_id,
            "creation_date": self.creation_date,
            "type": self.type
        }

    def serialize_content(self):
        products, boxes = [], []
        for product in self.product_mappings:
            curr_product = product.product.serialize()
            curr_mapping = product.serialize()

            curr_product.update(curr_mapping)
            curr_product.pop("storage")
            products.append(curr_product)

        for box in self.boxes:
            curr_box = box.serialize()
            boxes.append(curr_box)
        return {
            "products": products,
            "boxes": boxes
        }


@dataclass
class Box(db.Model):
    __tablename__ = "box"
    id: int = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name: str = db.Column(db.String(65535), nullable=False)
    location_id: int = db.Column(db.Integer, db.ForeignKey("location.id", ondelete="SET NULL"), nullable=True)
    household_id: int = db.Column(db.Integer, db.ForeignKey("household.id"), nullable=False)
    creation_date: datetime = db.Column(db.DateTime, default=datetime.utcnow())
    type: int = db.Column(db.Integer, default=int(ContainerTypes.Box))

    product_mappings = db.relationship("ProductContainerMapping", back_populates="box", **box_product_conditions)
    location: Mapped[Location] = db.relationship("Location", back_populates="boxes")

    def serialize(self):
        return {
            "id": self.id,
            "name": self.name,
            "location": self.location.serialize() if self.location is not None else None,
            "household_id": self.household_id,
            "creation_date": self.creation_date,
            "type": self.type
        }

    def serialize_content(self):
        products = []
        for product in self.product_mappings:
            curr_product = product.product.serialize()
            curr_mapping = product.serialize()

            curr_product.update(curr_mapping)
            curr_product.pop("storage")

            products.append(curr_product)

        return products

