from fastapi.testclient import TestClient
from sqlmodel import Session, select

from ih.core.config import get_app_settings, BASE_DIR
from ih.db.db_setup import engine
from ih.db.models.User import User
from ih.schema.user.user import UserCreate


def test_registration_disabled(client: TestClient, monkeypatch):
    monkeypatch.setenv("IH_REGISTRATION_ALLOWED", "False")
    get_app_settings.cache_clear()
    assert get_app_settings().DB_URL.startswith("sqlite")
    registration = UserCreate(
        email="test@test.com",
        username="test",
        password="123456789",
        password_confirmation="123456789",
        first_name="Test",
        last_name="Test"
    )

    response = client.post("/api/user/register/", json=registration.model_dump(by_alias=True))
    assert response.status_code == 403
    assert response.json()["detail"] == "Registration is currently disabled. Contact this instance's administrator for more information"


def test_registration(client: TestClient, monkeypatch):
    monkeypatch.setenv("IH_REGISTRATION_ALLOWED", "True")
    get_app_settings.cache_clear()
    assert get_app_settings().DB_URL.startswith("sqlite")
    registration = UserCreate(
        email="test@test.com",
        username="test",
        password="123456789",
        password_confirmation="123456789",
        first_name="Test",
        last_name="Test"
    )

    response = client.post("/api/user/register/", json=registration.model_dump(by_alias=True))
    assert response.status_code == 201

    response = client.post("/api/user/register/", json=registration.model_dump(by_alias=True))
    assert response.status_code == 409
    assert response.json()["detail"] == {'message': 'email_already_exists', 'toast': False, 'toast_type': 'error'}

    registration.email = "test2@test.com"
    response = client.post("/api/user/register/", json=registration.model_dump(by_alias=True))
    assert response.status_code == 409
    assert response.json()["detail"] == {'message': 'username_already_exists', 'toast': False, 'toast_type': 'error'}

    with Session(engine) as session:
        to_delete = session.exec(select(User).where(User.username == registration.username)).first()
        if to_delete:
            session.delete(to_delete)
            session.commit()

