from enum import Enum
from fastapi import APIRouter, Depends
from ih.core.security.get_user import get_admin_user


class AdminAPIRouter(APIRouter):
    """Router for functions to be protected behind user authentication"""

    def __init__(self, tags: list[str | Enum] | None = None, prefix: str = "", **kwargs):
        super().__init__(tags=tags, prefix=prefix, dependencies=[Depends(get_admin_user)], **kwargs)
