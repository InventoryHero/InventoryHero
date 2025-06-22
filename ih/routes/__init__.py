from fastapi import APIRouter
from . import (
    auth, users, household, storage, items
)

router = APIRouter(prefix="/api")
router.include_router(users.router)
router.include_router(auth.router)
router.include_router(household.router)
router.include_router(storage.router)
router.include_router(items.router)