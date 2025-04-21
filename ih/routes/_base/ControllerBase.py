from abc import ABC
from functools import cached_property

from fastapi import Depends
from pydantic import ConfigDict
from sqlmodel import Session

from ih.core.logging.logger import get_logger
from ih.core.settings.settings import AppSettings
from ih.core.config import get_app_settings
from ih.db.db_setup import get_session
from ih.repositories.factory import RepositoryFactory


class ControllerBase(ABC):
    session: Session = Depends(get_session)

    @cached_property
    def settings(self) -> AppSettings:
        return get_app_settings()

    @property
    def household_id(self) -> int | None :
        return None

    @cached_property
    def repositories(self):
        return RepositoryFactory(self.session, None)

    @cached_property
    def logger(self):
        return get_logger()
