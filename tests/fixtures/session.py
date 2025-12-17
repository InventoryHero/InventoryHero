from collections.abc import Generator

import pytest
from sqlmodel import Session

from ih.db.db_setup import engine


@pytest.fixture(scope="module")
def session() -> Generator[Session, None, None]:

    with Session(engine) as session:
        yield session