from fastapi import APIRouter

from .product import router as product_base_router, product_scoped_router

router = APIRouter()

router.include_router(product_base_router, prefix="/products", tags=["products"])
router.include_router(product_scoped_router, prefix="/products", tags=["products"])