import hashlib
import secrets
from typing import Optional, List, Union
from uuid import UUID

from fastapi import HTTPException
from sqlalchemy import delete
from sqlalchemy.exc import IntegrityError

from sqlalchemy.orm import selectinload
from sqlmodel import Session, select
from starlette import status

from ih.db.models.User import User
from ih.db.models.households import Household
from ih.db.models.storage.Storage import StorageType, Storage
from ih.schema.storage.storage import StorageBaseSchema, StorageResponseSchema


class StorageRepository:
    session: Session
    user: Optional[User]
    household_id: Optional[UUID]

    def __init__(self, session: Session, user: Optional[User] = None, household: Optional[UUID] = None):
        self.session = session
        self.user = user
        self.household_id = household


    def create_storage(self, storage_type: StorageType, to_create: StorageBaseSchema) -> Storage:
        # todo check if to_create.parent_id exists and is in household
        parent = None
        if to_create.parent_id is not None:
            query = select(Storage).where(
                Storage.id == to_create.parent_id,
                Storage.household_id == self.household_id
            )
            parent = self.session.exec(query).first()

            if not parent:
                raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail="parent_not_found_in_household")

        match storage_type:
            case StorageType.BOX:
                if parent is None:
                    raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="box_needs_parent")
            case StorageType.ROOM:
                if parent is not None:
                    raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="room_cannot_have_parent")


        storage = Storage(
            name = to_create.name,
            parent_id = to_create.parent_id,
            storage_type=storage_type,
            household_id=self.household_id,
        )
        self.session.add(storage)
        self.session.commit()
        self.session.refresh(storage)
        return storage

    def get_all_storage(self, storage_type: StorageType) -> List[Storage]:
        return self.session.exec(select(Storage).where(Storage.storage_type == storage_type)).all()

