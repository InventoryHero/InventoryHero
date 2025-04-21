from fastapi import APIRouter

from . import register, user

router = APIRouter()

router.include_router(register.router, prefix="/user")

router.include_router(user.user_router)
router.include_router(user.admin_router)