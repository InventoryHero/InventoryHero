from backend.database import db
from enum import Enum
from dataclasses import dataclass
from sqlalchemy.orm import Mapped, backref
from datetime import datetime
from sqlalchemy.types import TypeDecorator, Integer


class ContainerTypes(int, Enum):
    All: int = -1
    NoContainer: int = 0
    Box: int = 1
    Location: int = 2

    def __int__(self):
        return self.value



class ContainerType(TypeDecorator):
    impl = Integer

    def process_bind_param(self, value, dialect):
        if isinstance(value, ContainerTypes):
            return value.value
        raise ValueError(f"Invalid ContainerTypes value: {value}")

    def process_result_value(self, value, dialect):
        return ContainerTypes(value)


@dataclass
class Storage(db.Model):
    __tablename__ = "storage"
    id: int = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name: str = db.Column(db.String(65535), nullable=False)
    storage_id: int = db.Column(db.Integer, db.ForeignKey("storage.id", ondelete="SET NULL"), nullable=True)
    household_id: int = db.Column(db.Integer, db.ForeignKey("household.id"), nullable=False)
    creation_date: datetime = db.Column(db.DateTime, default=datetime.utcnow())
    type: ContainerTypes = db.Column(ContainerType, default=ContainerTypes.Box)
    product_mappings = db.relationship("ProductContainerMapping", back_populates="storage")
    storage = db.relationship("Storage", remote_side=[id], backref=backref("children"))

    def serialize(self):
        data = {
            "id": self.id,
            "name": self.name,
            "household_id": self.household_id,
            "creation_date": self.creation_date,
            "products": len(self.product_mappings),
            "type": self.type
        }
        if self.type == ContainerTypes.Box and self.storage is not None:
            data["location"] = self.storage.serialize()
        return data

    def serialize_location(self):
        location_content = []
        for product in self.product_mappings:
            location_content.append({
                "type": "product",
                "id": f"product{product.id}",
                "content": product
            })

        for box in self.children:
            curr_box = box.serialize()
            location_content.append({
                "type": "box",
                "id": f"box{box.id}",
                "content": curr_box
            })
        return location_content

    def serialize_box(self):
        products = []
        for product in self.product_mappings:
            curr_product = product.product.serialize()
            curr_mapping = product.serialize()
            curr_product.update(curr_mapping)
            products.append(curr_product)

        return products

    def serialize_content(self):
        if self.type == ContainerTypes.Box:
            return self.serialize_box()
        if self.type == ContainerTypes.Location:
            return self.serialize_location()
