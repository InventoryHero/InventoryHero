import uuid
from typing import List

from fastapi_utils.cbv import cbv
from starlette import status

from ih.db.models.storage.Storage import StorageType
from ih.routes._base.StorageControllerBase import StorageControllerBase
from ih.routes._base.UserApiRouter import UserAPIRouter
from ih.schema.storage.storage import RoomCreateSchema, StorageResponseSchema

router = UserAPIRouter(prefix="", tags=["storage"])
scoped_router = UserAPIRouter(prefix="/content/{storage_id}", tags=["storage"])



@cbv(router)
class StorageBaseController(StorageControllerBase):

    @router.post("/", status_code=status.HTTP_201_CREATED)
    def create_storage(self, to_create: RoomCreateSchema):
        self.logger.warning(to_create)
        return self.repositories.storage.create_storage(to_create.storage_type, to_create)

    @router.get("/{storage_type}", status_code=status.HTTP_200_OK, response_model=List[StorageResponseSchema])
    def get_storages(self, storage_type: StorageType) -> List[StorageResponseSchema]:
        return self.repositories.storage.get_all_storage(storage_type)


@cbv(scoped_router)
class StorageScopedController(StorageControllerBase):

    @scoped_router.get("/")
    def list_items(self, storage_id: uuid.UUID):
        # logic here
        ...