from typing import Generator, Any

import pytest
from sqlmodel import Session, select
from ih.db.models.User import User  # adjust to your actual user model import
from ih.core.security.password import hash_password
from ih.db.db_setup import engine  # your shared engine

@pytest.fixture(scope="module")
def user() -> Generator[User, Any, None]:
    user = User(
        username="test1",
        email="test1@test1.com",
        confirmed=True,
        password=hash_password("test1"),
        admin=False,
        first_name="test1",
        last_name="test1"
    )

    with Session(engine) as session:
        session.add(user)
        session.commit()

        session.refresh(user)

        yield user
        existing_user = session.exec(select(User).where(User.id == user.id)).first()
        if existing_user:
            session.delete(user)
            session.commit()
