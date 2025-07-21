from fastapi import APIRouter

from . import public, user

router = APIRouter()

router.include_router(public.router)
router.include_router(user.user_router)
router.include_router(user.admin_router)