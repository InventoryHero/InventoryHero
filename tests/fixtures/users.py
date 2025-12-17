from typing import Generator, Any
import pytest
from sqlmodel import select
from ih.db.models.User import User
from ih.core.security.password import hash_password

@pytest.fixture(scope="function")
def user(session) -> Generator[User, Any, None]:
    user = User(
        username="test1",
        email="test1@test1.com",
        confirmed=True,
        password=hash_password("test1"),
        admin=False,
        first_name="test1",
        last_name="test1"
    )
    session.add(user)
    session.commit()

    session.refresh(user)
    yield user

    existing_user = session.exec(select(User).where(User.id == user.id)).first()
    if existing_user:
        session.delete(user)
        session.commit()
