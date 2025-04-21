from typing import Annotated

from fastapi import Depends
from sqlmodel import create_engine, Session

from ih.core.config import get_app_settings


settings = get_app_settings()

connect_args = {}
if "sqlite" in settings.DB_URL:
    connect_args["check_same_thread"] = False

engine = create_engine(settings.DB_URL, echo=False, connect_args=connect_args, pool_pre_ping=True, future=True)

def get_session():
    with Session(engine) as session:
        yield session


SessionDep = Annotated[Session, Depends(get_session)]