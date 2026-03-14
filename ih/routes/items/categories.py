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
from ih.schema.items import ItemSummarySchema, CategoryReadSchema, \
    CategoryCreateSchema

router = UserAPIRouter(prefix="", tags=["categories"])

@cbv(router)
class CategoryController(HouseholdContextController):

    @router.post("/create", status_code=status.HTTP_201_CREATED, response_model=CategoryReadSchema)
    def create_category(self, category: CategoryCreateSchema):
        return self.repositories.items.create_category(category)

    @router.get("/all", status_code=status.HTTP_200_OK, response_model=List[CategoryReadSchema])
    def get_categories(self) -> List[CategoryReadSchema]:
        return self.repositories.items.get_categories()