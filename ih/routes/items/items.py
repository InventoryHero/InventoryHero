import uuid
from collections import defaultdict
from functools import cached_property
from fastapi import HTTPException, Query

from typing import List, Optional, Tuple, Dict, Set

from fastapi import Path
from fastapi_utils.cbv import cbv
from sqlalchemy.exc import SQLAlchemyError
from starlette import status

from ih.routes._base.HouseholdContextController import HouseholdContextController
from ih.routes._base.UserApiRouter import UserAPIRouter
from ih.schema.common import BreadcrumbSchema
from ih.schema.items import ItemSummarySchema, ItemReadSchema, ItemCreateSchema, ItemInstanceCreate, \
    ItemInstanceReadSchema, ItemStorageReadSchema, ItemAttributesReadSchema, ItemDetailReadSchema, \
    ItemAttributesReadBaseSchema, ItemUpdateSchema, ItemStorageUpdateSchema, ItemAttributesUpdateSchema, \
    ItemInstanceUpdateSchema
from ih.schema.storage import StorageResponseSchema

router = UserAPIRouter(prefix="", tags=["items"])
product_scoped_router = UserAPIRouter(prefix="/{item_id}", tags=["items"])

@cbv(router)
class ItemBaseController(HouseholdContextController):

    @router.post("/create", status_code=status.HTTP_201_CREATED, response_model=ItemReadSchema)
    def create_product(self, item: ItemCreateSchema):
        self.logger.info(item)
        new_item = self.repositories.items.create(item)
        attribute = self.repositories.items.get_attribute(new_item.id, item.attributes)
        _ = self.repositories.items.create_instance(attribute.id, item.storage)
        return new_item

    @router.get("/overview", status_code=status.HTTP_200_OK, response_model=List[ItemSummarySchema])
    def get_products(self) -> List[ItemSummarySchema]:
        return self.repositories.items.get_items_summary()

@cbv(product_scoped_router)
class ItemController(HouseholdContextController):
    item_id: uuid.UUID = Path(...)

    @cached_property
    def item(self):
        item = self.repositories.items.get_by_id(self.item_id)
        if not item:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="product_not_found"
            )
        return item

    @product_scoped_router.post(
        "/create",
        response_model=ItemReadSchema, # Use your actual Pydantic schema
        status_code=status.HTTP_201_CREATED,
        summary="Create a new instance of a items"
    )
    def create_item_instance(self, instance_data: ItemInstanceCreate) -> ItemReadSchema:
        attribute = self.repositories.items.get_attribute(self.item.id, instance_data.attributes)
        product_storage = self.repositories.items.create_instance(attribute.id, instance_data.storage)
        product = self.item.model_dump()
        product["storage"] = product_storage
        return ItemInstanceReadSchema(**product, categories=self.item.categories)

    @product_scoped_router.get(
        "/",
        response_model=ItemDetailReadSchema,
        status_code=status.HTTP_200_OK,
        summary="Gets all stored instances of a items, grouped by their location, sorted by expiration date (if set)"
    )
    def get_item_instances(self,
                           from_storage: Optional[uuid.UUID] = Query(
                               None,
                               description="The ID of the storage location the user navigated from, used to build contextual breadcrumbs."
                           )
    ) -> ItemDetailReadSchema:
        """
        Retrieves all stored locations for a given items.

        The list is sorted to show items with the soonest expiration date first.
        Items with no expiration date are listed at the end.
        """

        results = self.repositories.items.get_item_instances(self.item.id, from_storage)
        print(results)

        attributes: Dict[uuid.UUID, ItemAttributesReadBaseSchema] = {}
        items: Dict[uuid.UUID, List[ItemStorageReadSchema]] = defaultdict(list)

        for result in results:
            for item_instance in result.item_locations:
                items[result.id].append(item_instance)
                attributes[item_instance.product_attribute_id] = item_instance.attributes

        breadcrumbs = self.repositories.storage.get_storage_path(from_storage)
        breadcrumbs = [BreadcrumbSchema(name=parent.name, id=parent.id, type=parent.storage_type) for parent in breadcrumbs]

        return ItemDetailReadSchema(
            **self.item.model_dump(),
            categories=self.item.categories,
            attributes=attributes,
            items=items,
            storage=results,
            breadcrumbs=breadcrumbs
        )

    @product_scoped_router.post(
        "/{item_storage_id}/consume",
        status_code=status.HTTP_204_NO_CONTENT,
        summary="Consume one instance of a items"
    )
    def consume_instance(self, item_storage_id: uuid.UUID) -> None:
        self.repositories.items.delete_instance(self.item.id, item_storage_id, False)

    @product_scoped_router.delete(
        "/{item_storage_id}",
        status_code=status.HTTP_204_NO_CONTENT,
        summary="Delete all instances of a items at a location"
    )
    def delete_instance(self, item_storage_id: uuid.UUID) -> None:
        self.repositories.items.delete_instance(self.item.id, item_storage_id, True)

    @product_scoped_router.delete(
        "/",
        status_code=status.HTTP_204_NO_CONTENT,
        summary="Delete whole item"
    )
    def delete(self) -> None:
        self.repositories.items.delete(self.item)
        
    @product_scoped_router.patch(
        "/",
        status_code=status.HTTP_200_OK,
        response_model=ItemReadSchema
    )
    def update(self, update_data: ItemUpdateSchema) -> ItemReadSchema:
        return self.repositories.items.update(self.item, update_data)

    @product_scoped_router.patch(
        "/{item_storage_id}",
        status_code=status.HTTP_204_NO_CONTENT,
        summary="Delete all instances of a items at a location"
    )
    def delete_instance(self,
                        item_storage_id: uuid.UUID,
                        update_data: ItemInstanceUpdateSchema
    ):
        if 'expiration_date' in update_data.attributes.model_fields_set:
            print("expiration_date was set")
        if 'quantity' in update_data.stock.model_fields_set:
            print("quantity was set")
        print(update_data.stock)
        print(update_data.attributes)

        self.repositories.items.update_instance(item_storage_id, update_data.attributes, update_data.stock)

# TODO MOVE INSTANCE TO DIFFERENT LOCATION


