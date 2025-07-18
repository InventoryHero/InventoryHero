
from typing import Optional, List
from uuid import UUID

from fastapi import HTTPException
from sqlalchemy import case
from sqlalchemy.orm import selectinload, joinedload, subqueryload, contains_eager
from sqlmodel import Session, select, func
from starlette import status

from ih.db.models import ItemStorage, Item, ItemAttributes, Category, Storage
from ih.db.models.User import User
from ih.db.models.storage.Storage import StorageType
from ih.schema.items import ItemSummarySchema, ItemCreateSchema, ItemAttributesCreateSchema, \
    ItemStorageCreateSchema, CategoryCreateSchema, ItemUpdateSchema, ItemAttributesUpdateSchema, ItemStorageUpdateSchema


class ItemRepository:
    session: Session
    user: Optional[User]
    household_id: Optional[UUID]

    def __init__(self, session: Session, user: Optional[User] = None, household: Optional[UUID] = None):
        self.session = session
        self.user = user
        self.household_id = household

    def get_by_name(self, name) -> Optional[Item]:
        stmt = (
            select(Item).where(Item.household_id == self.household_id, Item.name == name)
        )
        return self.session.exec(stmt).first()

    def get_by_id(self, item_id) -> Optional[Item]:
        stmt = (
            select(Item).where(Item.household_id == self.household_id, Item.id == item_id)
        )
        return self.session.exec(stmt).first()

    def get_attribute(
            self,
            item_id: UUID,
            attributes_data: Optional[ItemAttributesCreateSchema] = None
    ) -> Optional[ItemAttributes]:
        """
        Finds a items attribute by an exact match of its properties.

        Args:
            item_id: The ID of the parent items.
            attributes_data: A Pydantic schema with the attribute values to match.
                             If a field is provided, it's matched for equality.
                             If a field is omitted, it's matched for being NULL.

        Returns:
            The matching ProductAttribute object or None if no exact match is found.
        """

        if attributes_data is None:
            attributes_data = ItemAttributesCreateSchema()

        # Start with the mandatory filter for the item_id
        stmt = select(ItemAttributes).where(ItemAttributes.item_id == item_id)

        # Use the provided data, or an empty dictionary if none was given.
        search_criteria = attributes_data.model_dump() if attributes_data else {}
        for field_name in search_criteria:
            value = search_criteria[field_name]
            column = getattr(ItemAttributes, field_name)
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

        attribute = ItemAttributes(item_id=item_id, **attributes_data.model_dump())
        self.session.add(attribute)
        self.session.flush()
        self.session.refresh(attribute)
        return attribute

    def create_instance(self, attribute_id: UUID, storage: Optional[ItemStorageCreateSchema]):
        if storage is None:
            storage = ItemStorageCreateSchema()
        stmt = select(ItemStorage).where(
            ItemStorage.product_attribute_id == attribute_id,
            ItemStorage.storage_id == storage.storage_id,
        ).options(
            selectinload(ItemStorage.attributes)
        )

        product_storage = self.session.exec(stmt).first()
        if product_storage:
            product_storage.quantity += storage.quantity
            self.session.flush()
            self.session.refresh(product_storage)
            return product_storage

        storage = ItemStorage(product_attribute_id=attribute_id, storage_id=storage.storage_id, quantity=storage.quantity)
        self.session.add(storage)
        self.session.flush()
        self.session.refresh(storage)
        return storage

    def get_items_summary(self, storage_id: Optional[UUID] = None) -> List[ItemSummarySchema]:
        stmt = (
            select(
                Item,
                func.coalesce(func.sum(ItemStorage.quantity), 0).label("total_quantity")
            )
            .outerjoin(ItemAttributes, Item.id == ItemAttributes.item_id)
            .outerjoin(ItemStorage, ItemAttributes.id == ItemStorage.product_attribute_id)
            .where(Item.household_id == self.household_id)
            .options(subqueryload(Item.categories))
        )

        if storage_id is not None:
            stmt = stmt.where(ItemStorage.storage_id == storage_id)

        stmt = stmt.group_by(Item.id)
        results = self.session.exec(stmt).all()
        return [ItemSummarySchema(**product.model_dump(), categories=product.categories, total_quantity=quantity) for (product, quantity) in results]


    def create(self, to_create: ItemCreateSchema) -> Item:
        existing = self.get_by_name(to_create.name)
        if existing:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="product_already_exists")

        product = Item(**to_create.model_dump(exclude={"categories", "attributes", "storage"}), household_id=self.household_id)

        for category_id in to_create.categories:
            stmt = (
                select(Category)
                .where(Category.id == category_id, Category.household_id == self.household_id)
            )

            category = self.session.exec(stmt).first()
            if category is None:
                continue
            product.categories.append(category)

        self.session.add(product)
        self.session.flush()
        self.session.refresh(product)
        return product

    def get_item_instances(self, item_id: UUID, from_storage_id: Optional[UUID] = None) -> List[ItemStorage]:
        order_clauses = []
        if from_storage_id:
            order_clauses.append(
                case(
                    (Storage.id == from_storage_id, 0),  # If ID matches, priority = 0
                    else_=1  # Otherwise, priority = 1
                ).asc()
             )

        order_clauses.append(
            case(
                (Storage.storage_type == StorageType.BOX, 2),
                (Storage.storage_type == StorageType.ROOM, 1),
                else_=99  # A fallback for any other types to appear last
            ).asc()
        )
        order_clauses.append(Storage.name.asc())

        stmt = (
            # Start by selecting the model you want a list of at the end
            select(Storage)
            .join(ItemStorage)
            .join(ItemAttributes)
            .join(Item)
            .where(
                ItemAttributes.item_id == item_id, 
                Item.household_id == self.household_id
            )

            .order_by(*order_clauses)

            .options(
                contains_eager(Storage.item_locations)
                .contains_eager(ItemStorage.attributes)
            )
        )

        # Execute the query to get a list of ProductLocation ORM objects
        results = self.session.exec(stmt).unique().all()
        return results

    def delete_instance(self, item_id: UUID, location_id: UUID, all: bool = False) -> None:
        stmt = (
            select(ItemStorage)
            .join(ItemAttributes, ItemStorage.product_attribute_id == ItemAttributes.id)
            .join(Item, Item.id == ItemAttributes.item_id)
            .where(Item.id == item_id, ItemStorage.id == location_id)
        )
        instance = self.session.exec(stmt).first()

        if instance is None:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="product_not_found")

        if not all:
            instance.quantity = max(0, instance.quantity - 1)
            return
        attribute_id = instance.product_attribute_id
        remaining_locations_stmt = (
            select(func.count(ItemStorage.id))
            .where(ItemStorage.product_attribute_id == attribute_id)
        )
        self.session.delete(instance)
        self.session.flush()

        remaining_locations = self.session.exec(remaining_locations_stmt).all()
        print(remaining_locations)
        if len(remaining_locations) > 0:
            return
        attribute = self.session.exec(select(ItemAttributes).where(ItemAttributes.id == attribute_id)).first()
        if attribute:
            self.session.delete(attribute)

    def create_category(self, category: CategoryCreateSchema) -> Category:
        stmt = (
            select(Category)
            .where(Category.household_id == self.household_id, Category.name == category.name)
        )
        result = self.session.exec(stmt).first()
        if result is not None:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="category_already_exists")
        category = Category(**category.model_dump(), household_id=self.household_id)
        self.session.add(category)
        self.session.flush()
        self.session.refresh(category)
        return category

    def get_categories(self) -> List[Category]:
        stmt = (
            select(Category)
            .where(Category.household_id == self.household_id)
        )
        return self.session.exec(stmt)

    def delete(self, item: Item):
        self.session.delete(item)
        self.session.flush()

    def update(self, item: Item, update_data: ItemUpdateSchema) -> Item:
        if update_data.name is not None:
            item.name = update_data.name

        if update_data.description is not None:
            item.description = update_data.description

        if update_data.categories_to_remove:
            item.categories = [
                cat for cat in item.categories if cat.id not in update_data.categories_to_remove
            ]



        if update_data.categories_to_add:
            new_categories = self.session.exec(
                select(Category)
                .where(Category.id.in_(update_data.categories_to_add), Category.household_id == self.household_id)
            ).all()
            existing_ids = {cat.id for cat in item.categories}
            # Filter out ones already linked
            for category in new_categories:
                if category.id not in existing_ids:
                    item.categories.append(category)

        # Handle category removals


        self.session.add(item)
        self.session.flush()
        self.session.refresh(item)
        return item

    def update_instance(self, instance_id: UUID, attributes_to_update: ItemAttributesUpdateSchema, item_stock: ItemStorageUpdateSchema) -> None:
        # first check if there are other instances with the same attributes in the household
        # if no, we need to create a new attribute set, otherwise we can reuse the old one
        # check the item_stock to update

        instance = self.session.exec(
            select(ItemStorage)
            .join(ItemAttributes)
            .join(Item)
            .where(
                ItemStorage.id == instance_id,
                Item.household_id == self.household_id,
            )
        ).first()

        if instance is None:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="item_not_found"
            )

        curr_attributes = self.session.exec(
            select(ItemAttributes)
            .where(ItemAttributes.id == instance.product_attribute_id)
        ).first()

        if curr_attributes is None:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="unknown_error_occurred"
            )


        stmt = select(ItemAttributes).where(ItemAttributes.item_id == curr_attributes.item_id)

        # Use the provided data, or an empty dictionary if none was given.
        search_criteria = attributes_to_update.model_dump()
        original_attributes = curr_attributes.model_dump()
        for field_name in search_criteria:
            column = getattr(ItemAttributes, field_name)
            value = search_criteria[field_name]

            if field_name in attributes_to_update.model_fields_set:
                condition_value = value
            else:
                condition_value = original_attributes[field_name]

            if condition_value is None:
                stmt = stmt.where(column.is_(None))
            else:
                stmt = stmt.where(column == condition_value)

        new_attributes = self.session.exec(stmt).first()
        print(new_attributes)
        if new_attributes is None:

            new_attributes = ItemAttributes(**attributes_to_update.model_dump(), item_id=curr_attributes.item_id)
            self.session.add(new_attributes)
            self.session.flush()
            self.session.refresh(new_attributes)

        # now that we have the attributes, we need to check if this attribute set is already stored at this location
        stmt = (
            select(ItemStorage)
            .where(
                ItemStorage.product_attribute_id == new_attributes.id,
                ItemStorage.storage_id == instance.storage_id
            )
        )
        new_instance = self.session.exec(stmt).first()

        if new_instance is None:
            new_instance = ItemStorage(
                storage_id = instance.storage_id,
                product_attribute_id = new_attributes.id
            )
            print(new_instance)
            self.session.add(new_instance)
            self.session.flush()
            self.session.refresh(new_instance)
        print("HALLO")
        if 'quantity' not in item_stock.model_fields_set:
            item_stock.quantity = instance.quantity

        new_instance.quantity += item_stock.quantity

        self.session.delete(instance)




