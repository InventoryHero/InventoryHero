from fastapi import APIRouter

from .categories import router as categories_router
from .items import router as product_base_router, product_scoped_router

router = APIRouter()

router.include_router(product_base_router, prefix="/items", tags=["items"])
router.include_router(product_scoped_router, prefix="/items", tags=["items"])

router.include_router(categories_router, prefix="/categories", tags=["categories"])