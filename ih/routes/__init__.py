from fastapi import APIRouter
from . import users
from . import auth
from . import household
from . import storage

router = APIRouter(prefix="/api")
router.include_router(users.router)
router.include_router(auth.router)
router.include_router(household.router)
router.include_router(storage.router)