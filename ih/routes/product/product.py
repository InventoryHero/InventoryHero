import uuid
from functools import cached_property
from fastapi import HTTPException

from typing import List, Optional

from fastapi import Path
from fastapi_utils.cbv import cbv
from sqlalchemy.exc import SQLAlchemyError
from starlette import status

from ih.routes._base.HouseholdContextController import HouseholdContextController
from ih.routes._base.UserApiRouter import UserAPIRouter
from ih.schema.products import ProductSummarySchema, ProductReadSchema, ProductCreateSchema, ProductInstanceCreate, \
    ProductInstanceReadSchema, ProductStorageRead, ProductAttributeReadSchema

router = UserAPIRouter(prefix="", tags=["products"])
product_scoped_router = UserAPIRouter(prefix="/{product_id}", tags=["products"])

@cbv(router)
class ProductBaseController(HouseholdContextController):

    @router.post("/create", status_code=status.HTTP_201_CREATED, response_model=ProductReadSchema)
    def create_product(self, product: ProductCreateSchema):
        return self.repositories.products.create(product)

    @router.get("/overview", status_code=status.HTTP_200_OK, response_model=List[ProductSummarySchema])
    def get_products(self) -> List[ProductSummarySchema]:
        return self.repositories.products.get_product_summary()

@cbv(product_scoped_router)
class ProductScopedController(HouseholdContextController):
    product_id: uuid.UUID = Path(...)

    @cached_property
    def product(self):
        self.logger.info("fml")
        product = self.repositories.products.get_by_id(self.product_id)
        self.logger.info(product)
        if not product:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="product_not_found"
            )
        return product

    @product_scoped_router.post(
        "/create",
        response_model=Optional[ProductInstanceReadSchema], # Use your actual Pydantic schema
        status_code=status.HTTP_201_CREATED,
        summary="Create a new instance of a product",
        description="""
            Creates one or more instances of a product. This endpoint flexibly handles
            the creation of an item with specific attributes, a storage location, or both.

            - **Provide `attributes` and `location`:** Creates a specific, tracked item and places it in storage.
            - **Provide only `attributes`:** Creates a tracked item that is not yet in a storage location (i.e., it's "in the void").
            - **Provide only `location`:** Creates a default instance of the item and places it directly in storage.
            """
    )

    def create_product_instance(self, instance_data: ProductInstanceCreate) -> Optional[ProductInstanceReadSchema]:
        self.logger.warning(self.product)
        attribute = self.repositories.products.get_attribute(self.product.id, instance_data.attributes)
        self.logger.warning(attribute)

        product_storage = self.repositories.products.create_instance(attribute.id, instance_data.storage)
        self.logger.warning(product_storage)

        product = self.product.model_dump()
        product["storage"] = product_storage

        try:
            self.session.commit()
        except SQLAlchemyError as e:
            self.session.rollback()
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=str(e)
            )
        return ProductInstanceReadSchema(**product)

    @product_scoped_router.get(
        "/",
        response_model=List[ProductAttributeReadSchema],
        status_code=status.HTTP_200_OK,
        summary="Gets all stored instances of a product, grouped by their location, sorted by expiration date (if set)"
    )
    def get_product_instances(self) -> List[ProductAttributeReadSchema]:
        """
        Retrieves all stored locations for a given product.

        The list is sorted to show items with the soonest expiration date first.
        Items with no expiration date are listed at the end.
        """

        results = self.repositories.products.get_product_instances(self.product.id)

        # FastAPI will automatically take this list of ORM objects and parse it
        # into a list of your `ProductStorageRead` Pydantic schemas because
        # you've defined the `response_model` and enabled `from_attributes`.
        return results

    @product_scoped_router.post(
        "/{location_id}/consume",
        status_code=status.HTTP_204_NO_CONTENT,
        summary="Consume one instance of a product"
    )
    def consume_instance(self, location_id: uuid.UUID) -> None:
        self.repositories.products.delete_instance(self.product.id, location_id, False)

    @product_scoped_router.delete(
        "/{location_id}",
        status_code=status.HTTP_204_NO_CONTENT,
        summary="Delete all instances of a product at a location"
    )
    def delete_instance(self, location_id: uuid.UUID) -> None:
        self.repositories.products.delete_instance(self.product.id, location_id, True)

