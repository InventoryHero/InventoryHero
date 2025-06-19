
from typing import Optional, List
from uuid import UUID

from fastapi import HTTPException
from sqlalchemy.orm import selectinload
from sqlmodel import Session, select, func
from starlette import status

from ih.db.models import ProductLocation, Product, ProductAttribute
from ih.db.models.User import User
from ih.schema.products import ProductSummarySchema, ProductCreateSchema, ProductAttributeCreateSchema, \
    ProductStorageCreate


class ProductRepository:
    session: Session
    user: Optional[User]
    household_id: Optional[UUID]

    def __init__(self, session: Session, user: Optional[User] = None, household: Optional[UUID] = None):
        self.session = session
        self.user = user
        self.household_id = household

    def get_by_name(self, name) -> Optional[Product]:
        stmt = (
            select(Product).where(Product.household_id == self.household_id, Product.name == name)
        )
        return self.session.exec(stmt).first()

    def get_by_id(self, product_id) -> Optional[Product]:
        stmt = (
            select(Product).where(Product.household_id == self.household_id, Product.id == product_id)
        )
        return self.session.exec(stmt).first()

    def get_attribute(
            self,
            product_id: UUID,
            attributes_data: Optional[ProductAttributeCreateSchema] = None
    ) -> Optional[ProductAttribute]:
        """
        Finds a product attribute by an exact match of its properties.

        Args:
            product_id: The ID of the parent product.
            attributes_data: A Pydantic schema with the attribute values to match.
                             If a field is provided, it's matched for equality.
                             If a field is omitted, it's matched for being NULL.

        Returns:
            The matching ProductAttribute object or None if no exact match is found.
        """

        # if there is no attributes_data specified by the user, use the default one
        if attributes_data is None:
            attributes_data = ProductAttributeCreateSchema()

        # Start with the mandatory filter for the product_id
        stmt = select(ProductAttribute).where(ProductAttribute.product_id == product_id)

        # Use the provided data, or an empty dictionary if none was given.
        search_criteria = attributes_data.model_dump() if attributes_data else {}
        for field_name in search_criteria:
            value = search_criteria[field_name]
            column = getattr(ProductAttribute, field_name)
            if value is not None:
                # If the user provided a value, filter for equality.
                stmt = stmt.where(column == value)
            else:
                # If the user did NOT provide a value, filter for records
                # where that column is NULL in the database.
                stmt = stmt.where(column.is_(None))

        attribute = self.session.exec(stmt).first()
        if attribute:
            return attribute

        attribute = ProductAttribute(product_id=product_id, **attributes_data.model_dump())
        self.session.add(attribute)
        self.session.flush()
        self.session.refresh(attribute)
        return attribute

    def create_instance(self, attribute_id: UUID, storage: Optional[ProductStorageCreate]):
        if storage is None:
            storage = ProductStorageCreate()
        stmt = select(ProductLocation).where(
            ProductLocation.product_attribute_id == attribute_id,
            ProductLocation.storage_id == storage.storage_id,
        ).options(
            selectinload(ProductLocation.attributes)
        )

        product_storage = self.session.exec(stmt).first()
        if product_storage:
            product_storage.quantity += storage.quantity
            self.session.flush()
            self.session.refresh(product_storage)
            return product_storage

        storage = ProductLocation(product_attribute_id=attribute_id, storage_id=storage.storage_id, quantity=storage.quantity)
        self.session.add(storage)
        self.session.flush()
        self.session.refresh(storage)
        return storage

    def get_product_summary(self) -> List[ProductSummarySchema]:
        stmt = (
            select(
                Product,
                func.coalesce(func.sum(ProductLocation.quantity), 0).label("total_quantity")
            )
            .outerjoin(ProductAttribute, Product.id == ProductAttribute.product_id)
            .outerjoin(ProductLocation, ProductAttribute.id == ProductLocation.product_attribute_id)
            .where(Product.household_id == self.household_id)
            .group_by(Product.id)
        )
        results = self.session.exec(stmt).all()
        return [ProductSummarySchema(**product.model_dump(), total_quantity=quantity) for (product, quantity) in results]

    def create(self, to_create: ProductCreateSchema) -> Product:
        existing = self.get_by_name(to_create.name)
        if existing:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="product_already_exists")
        product = Product(**to_create.model_dump(), household_id=self.household_id)
        self.session.add(product)
        self.session.commit()
        self.session.refresh(product)
        return product

    def get_product_instances(self, product_id: UUID) -> List[ProductAttribute]:
        # This query selects all ProductLocation entries that are linked,
        # via the ProductAttribute table, to the product_id from the URL.
        stmt = (
            select(ProductAttribute)
            .join(ProductLocation)
            .where(ProductAttribute.product_id == product_id)
            .order_by(ProductAttribute.expiration_date.asc().nullslast())
            .group_by(ProductAttribute.id)
            .options(
                # Eagerly load the related attribute for each location.
                # This prevents N+1 query problems and is crucial for performance.
                selectinload(ProductAttribute.storage)
            )
        )

        # Execute the query to get a list of ProductLocation ORM objects
        results = self.session.exec(stmt).all()
        return results

    def delete_instance(self, product_id: UUID, location_id: UUID, all: bool = False) -> None:
        stmt = (
            select(ProductLocation)
            .join(ProductAttribute, ProductLocation.product_attribute_id == ProductAttribute.id)
            .join(Product, Product.id == ProductAttribute.product_id)
            .where(Product.id == product_id, ProductLocation.id == location_id)
        )
        instance = self.session.exec(stmt).first()

        if instance is None:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="product_not_found")

        if not all:
            instance.quantity = max(0, instance.quantity - 1)
            return
        attribute_id = instance.product_attribute_id
        remaining_locations_stmt = (
            select(func.count(ProductLocation.id))
            .where(ProductLocation.product_attribute_id == attribute_id)
        )
        self.session.delete(instance)
        self.session.flush()

        remaining_locations = self.session.exec(remaining_locations_stmt).one()
        if remaining_locations > 0:
            return
        attribute = self.session.exec(select(ProductAttribute).where(ProductAttribute.id == attribute_id)).first()
        if attribute:
            self.session.delete(attribute)




