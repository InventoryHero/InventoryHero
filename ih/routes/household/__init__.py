from fastapi import APIRouter

from .household import router as crud_router
from .member import router as member_router
from .invite import router as invite_router, accept_invite_router

router = APIRouter()
router.include_router(crud_router)
router.include_router(member_router, prefix="/household")
router.include_router(invite_router, prefix="/household")
router.include_router(accept_invite_router, prefix="/household")