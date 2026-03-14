from typing import Annotated

from fastapi import Depends, HTTPException
from sqlalchemy.exc import SQLAlchemyError
from sqlmodel import create_engine, Session

from ih.core.config import get_app_settings

from sqlmodel import Field, Relationship, Session, SQLModel, create_engine, MetaData

# 1. Define the same naming convention dictionary
naming_convention = {
    "ix": "ix_%(column_0_label)s",
    "uq": "uq_%(table_name)s_%(column_0_name)s",
    "ck": "ck_%(table_name)s_%(constraint_name)s",
    "fk": "fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s",
    "pk": "pk_%(table_name)s"
}

# 2. Apply it directly to the SQLModel metadata object
SQLModel.metadata.naming_convention = naming_convention

settings = get_app_settings()

connect_args = {}
if "sqlite" in settings.DB_URL:
    connect_args["check_same_thread"] = False

engine = create_engine(settings.DB_URL, echo=False, connect_args=connect_args, pool_pre_ping=True, future=True)

def get_session():
    with Session(engine) as session:
        try:
            yield session
            session.commit()
        except SQLAlchemyError as e:
            print(e)
            session.rollback()
            raise HTTPException(status_code=500, detail=str(e))



SessionDep = Annotated[Session, Depends(get_session)]