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

    @property
    def serialize(self):
        storage = {
            "id": self.id,
            "name": self.name,
            "storageId": self.storage_id,
            "householdId": self.household_id,
            "creationDate": self.creation_date,
            "storage": self.storage if self.storage else None,
            "productAmount": len(self.product_mappings),
            "type": self.type
        }
        if self.type == ContainerTypes.Location:
            storage["boxAmount"] = len(self.children)
        return storage





