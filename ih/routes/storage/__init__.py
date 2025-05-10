from fastapi import APIRouter

from .storage import (
    router as storage_base_router,
    scoped_router as storage_scoped_router
)

router = APIRouter()

router.include_router(storage_base_router, prefix="/storage", tags=["storage"])
router.include_router(storage_scoped_router, prefix="/storage", tags=["storage"])