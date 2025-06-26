import uuid
from functools import cached_property
from typing import List, Any, Optional

from fastapi import Path, HTTPException, Query
from fastapi_utils.cbv import cbv
from starlette import status

from ih.db.models.storage.Storage import StorageType
from ih.routes._base.HouseholdContextController import HouseholdContextController
from ih.routes._base.UserApiRouter import UserAPIRouter
from ih.schema.items import ItemSummarySchema

from ih.schema.storage import StorageResponseSchema, StorageCreateSchema, AnyStorageResponse, ContentType, \
    BoxResponseSchema, RoomResponseSchema

router = UserAPIRouter(prefix="", tags=["storage"])
scoped_router = UserAPIRouter(prefix="/{storage_id}", tags=["storage"])



@cbv(router)
class StorageBaseController(HouseholdContextController):

    @router.post("/create", status_code=status.HTTP_201_CREATED)
    def create_storage(self, to_create: StorageCreateSchema) -> StorageResponseSchema:
        self.logger.warning(to_create)
        return self.repositories.storage.create_storage(to_create.storage_type, to_create)

    @router.get(
        "/all",
        status_code=status.HTTP_200_OK,
        response_model=List[AnyStorageResponse],
        response_model_exclude_none=True
    )
    def get_all(self,
                storage_type: Optional[StorageType] = Query(
                    None,
                    description="Filter the results by storage type. Omit to get all storage")
    ) -> List[AnyStorageResponse]:

        match storage_type:
            case StorageType.ROOM:
                return self.repositories.storage.list_rooms()
            case StorageType.BOX:
                return self.repositories.storage.list_boxes()
            case _:
                return self.repositories.storage.get_storage()



@cbv(scoped_router)
class StorageScopedController(HouseholdContextController):
    storage_id: uuid.UUID = Path(...)

    @cached_property
    def storage(self):
        storage = self.repositories.storage.get_by_id(self.storage_id)
        self.logger.warning(storage)
        if not storage:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"storage_not_found"
            )
        return storage

    @scoped_router.get(
        "/detail",
        status_code=status.HTTP_200_OK,
        response_model=AnyStorageResponse,
        response_model_exclude_none=True
    )
    def get_detail(self) -> AnyStorageResponse:
        match self.storage.storage_type:
            case StorageType.ROOM:
                return RoomResponseSchema(**self.storage.model_dump())
            case StorageType.BOX:
                return BoxResponseSchema(**self.storage.model_dump(), parent=self.storage.parent)
            case _:
                raise HTTPException(
                    status_code=status.HTTP_501_NOT_IMPLEMENTED,
                    detail=f"storage_{self.storage.storage_type}_not_support"
                )


    @scoped_router.get(
        "/items",
        status_code=status.HTTP_200_OK,
        response_model=List[ItemSummarySchema],
        response_model_exclude_none=True
    )
    def get_items(self) -> List[ItemSummarySchema]:
        return self.repositories.items.get_items_summary(self.storage.id)

    @scoped_router.get(
        "/boxes",
        status_code=status.HTTP_200_OK,
        response_model=List[BoxResponseSchema],
        response_model_exclude_none=True
    )
    def get_boxes(self) -> BoxResponseSchema:
        if self.storage.storage_type == StorageType.BOX:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="box_has_only_items"
            )
        return self.repositories.storage.list_boxes(self.storage.id)


