from fastapi import APIRouter

from .routes import router as config_router

router = APIRouter()
router.include_router(config_router, prefix="/config", tags=["config"])
