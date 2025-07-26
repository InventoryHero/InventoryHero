import hashlib
import secrets
from typing import Optional, List, Union, Any, Sequence
from uuid import UUID

from fastapi import HTTPException
from sqlalchemy import delete, func, Row, RowMapping, literal
from sqlalchemy.exc import IntegrityError

from sqlalchemy.orm import selectinload, aliased, noload
from sqlmodel import Session, select
from sqlmodel.sql._expression_select_cls import _T
from starlette import status

from ih.db.models import Item, ItemStorage, ItemAttributes
from ih.db.models.User import User
from ih.db.models.households import Household
from ih.db.models.storage.Storage import StorageType, Storage
from ih.schema.items import ItemInstanceReadSchema
from ih.schema.storage.storage import StorageBaseSchema, StorageResponseSchema, BoxResponseSchema, RoomResponseSchema, \
    AnyStorageUpdateSchema, BoxUpdateSchema


class StorageRepository:
    session: Session
    user: Optional[User]
    household_id: Optional[UUID]

    def __init__(self, session: Session, user: Optional[User] = None, household: Optional[UUID] = None):
        self.session = session
        self.user = user
        self.household_id = household


    def get_by_id(self, storage_id: UUID) -> Optional[Storage]:
        stmt = (
            select(Storage)
            .where(
                Storage.household_id == self.household_id,
                Storage.id == storage_id
            )
            .options(selectinload(Storage.parent))
        )
        return self.session.exec(stmt).first()

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
                if parent is None and to_create.parent_id is not None:
                    raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="box_needs_room_parent")
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
        self.session.flush()
        self.session.refresh(storage)
        print(storage)
        return storage

    def get_storage(self) -> List[Storage]:
        stmt = (
            select(Storage)
            .where(
                Storage.household_id == self.household_id
            )
            .order_by(Storage.storage_type, Storage.name)  # Good to sort it for the dropdown
            .options(noload(Storage.parent))
        )
        return self.session.exec(stmt).all()

    def list_boxes(self, storage_id: Optional[UUID] = None) -> List[BoxResponseSchema]:
        item_counts_sq = (
            select(
                ItemStorage.storage_id.label("storage_id"),
                func.sum(ItemStorage.quantity).label("num_items")
            )
            .group_by(ItemStorage.storage_id)
            .subquery()
        )

        stmt = (
            select(
                Storage,
                func.coalesce(item_counts_sq.c.num_items, 0).label("num_items")
            )
            .outerjoin(item_counts_sq, Storage.id == item_counts_sq.c.storage_id)

            .where(
                Storage.household_id == self.household_id,
                Storage.storage_type == StorageType.BOX,

            )
        )

        if storage_id is not None:
            stmt = stmt.where(Storage.parent_id == storage_id)

        results = self.session.exec(stmt).all()
        return [BoxResponseSchema(**box.model_dump(), num_items=num_items, parent=None) for box, num_items in results]


    def list_rooms(self) -> List[RoomResponseSchema]:
        item_counts_sq = (
            select(
                ItemStorage.storage_id.label("storage_id"),
                func.sum(ItemStorage.quantity).label("num_items")
            )
            .group_by(ItemStorage.storage_id)
            .subquery()
        )
        box_counts_sq = (
            select(
                Storage.parent_id.label("parent_id"),
                func.count(Storage.id).label("num_boxes")
            )
            .where(Storage.storage_type == StorageType.BOX)
            .group_by(Storage.parent_id)
            .subquery()
        )

        stmt = (
            select(
                Storage,
                func.coalesce(item_counts_sq.c.num_items, 0).label("num_items"),
                func.coalesce(box_counts_sq.c.num_boxes, 0).label("num_boxes")
            )
            .outerjoin(item_counts_sq, Storage.id == item_counts_sq.c.storage_id)
            .outerjoin(box_counts_sq, Storage.id == box_counts_sq.c.parent_id)
            .order_by(Storage.name)
            .where(
                Storage.household_id == self.household_id,
                Storage.storage_type == StorageType.ROOM,

            )
        )

        results = self.session.exec(stmt).all()
        return [RoomResponseSchema(**room.model_dump(), num_items=num_items, num_boxes=num_boxes) for room, num_items, num_boxes in results]


    def get_storage_path(self, starting_storage_id: UUID) -> List[Storage]:
        """
        Uses a recursive CTE to fetch the full hierarchical path for a given storage ID.
        Returns the path from the top-most parent to the starting node.
        """
        if not starting_storage_id:
            return []

        # Alias the Storage model to use in the CTE
        storage_alias = aliased(Storage)

        # Create the CTE object
        # The name 'storage_path_cte' is arbitrary
        path_cte = (
            select(Storage, literal(0).label('depth'))
            .where(Storage.id == starting_storage_id)
            .cte(name="storage_path_cte", recursive=True)
        )

        # Define the recursive part of the CTE
        # This joins the CTE to the Storage table to find the parent
        recursive_part = (
            select(storage_alias, path_cte.c.depth + 1)
            .join(path_cte, path_cte.c.parent_id == storage_alias.id)
        )

        # Combine the anchor and recursive parts with UNION ALL
        full_cte = path_cte.union_all(recursive_part)

        # Now, select everything from our completed CTE
        stmt = (
            select(Storage)
            .join(full_cte, Storage.id == full_cte.c.id)
            .order_by(full_cte.c.depth.desc())  # Order by depth to get Grandparent -> Parent -> Child
        )

        # Execute the query
        results = self.session.exec(stmt).all()
        return results

    def delete_storage(self, storage: Storage) -> None:
        self.session.delete(storage)
        self.session.flush()

    def update_storage(self, storage: Storage, update_data: AnyStorageUpdateSchema):
        # update name
        if 'name' in update_data.model_fields_set:
            storage.name = update_data.name

        if isinstance(update_data, BoxUpdateSchema) and 'parent_id' in update_data.model_fields_set:
            parent_id = update_data.parent_id
            new_parent = self.session.exec(
                select(Storage).where(Storage.id == parent_id, Storage.household_id == self.household_id)
            ).first()
            if new_parent is not None and new_parent.storage_type != "box":
                storage.parent_id = new_parent.id
                print("hallo", storage.parent_id)

        self.session.flush()
        self.session.refresh(storage)
