from fastapi import APIRouter

from .routes import router as config_router, admin_router

router = APIRouter()
router.include_router(config_router, prefix="/config", tags=["config"])
router.include_router(admin_router, prefix="/admin/config", tags=["app admin"])
