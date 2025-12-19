import hashlib

from fastapi.testclient import TestClient
from sqlmodel import Session, select

from ih.core.config import get_app_settings, BASE_DIR
from ih.db.db_setup import engine
from ih.db.models.User import User
from ih.schema.user.user import UserCreate
from tests.utils.email import parse_email_messages, clear_messages


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


def test_registration_without_smtp(client: TestClient, monkeypatch, session):
    monkeypatch.setenv("IH_REGISTRATION_ALLOWED", "True")
    monkeypatch.setenv("IH_SMTP_HOST", "")
    get_app_settings.cache_clear()
    assert get_app_settings().DB_URL.startswith("sqlite")
    assert not get_app_settings().IH_SMTP_ENABLED
    registration = UserCreate(
        email="test@test.com",
        username="test",
        password="123456789",
        password_confirmation="123456789",
        first_name="Test",
        last_name="Test"
    )

    response = client.post("/api/user/register/", json=registration.model_dump(by_alias=True))
    assert response.status_code == 204

    response = client.post("/api/user/register/", json=registration.model_dump(by_alias=True))
    assert response.status_code == 409
    assert response.json()["detail"] == {'message': 'email_already_exists', 'toast': False, 'toast_type': 'error'}

    registration.email = "test2@test.com"
    response = client.post("/api/user/register/", json=registration.model_dump(by_alias=True))
    assert response.status_code == 409
    assert response.json()["detail"] == {'message': 'username_already_exists', 'toast': False, 'toast_type': 'error'}

    to_delete = session.exec(select(User).where(User.username == registration.username)).first()
    assert to_delete is not None
    session.delete(to_delete)
    session.commit()

def test_registration_with_smtp(client: TestClient, monkeypatch, session):
    monkeypatch.setenv("IH_REGISTRATION_ALLOWED", "True")
    monkeypatch.setenv("IH_SMTP_HOST", "localhost")
    get_app_settings.cache_clear()
    settings = get_app_settings()
    assert settings.DB_URL.startswith("sqlite")
    assert settings.IH_SMTP_ENABLED
    registration = UserCreate(
        email="test@test.com",
        username="test",
        password="123456789",
        password_confirmation="123456789",
        first_name="Test",
        last_name="Test"
    )

    response = client.post("/api/user/register/", json=registration.model_dump(by_alias=True))
    assert response.status_code == 204
    confirmation_code = parse_email_messages(registration.email, f"{settings.IH_APP_URL}/confirm/")
    user = session.exec(select(User).where(User.username == registration.username)).first()
    assert user is not None
    assert user.confirmation_code == hashlib.sha256(confirmation_code.encode()).hexdigest()
    clear_messages()

    form_data = {"username": user.username, "password": "123456789"}
    response = client.post("/api/auth/token", data=form_data)
    assert response.status_code == 200
    assert "set-cookie" in response.headers
    response = client.get(f"/api/user/request-confirmation")
    assert response.status_code == 204

    session.refresh(user)
    assert user.confirmation_code != confirmation_code

    # after requestîng a new code, the old code should be invalid
    response = client.post(f"/api/user/confirm-email/{confirmation_code}")
    assert response.status_code == 404
    data = response.json()["detail"]
    assert data["message"] == "The requested confirmation code could not be found. Either it expired, or it doesn't exist"
    assert data["toast"] is False

    confirmation_code = parse_email_messages(registration.email, f"{settings.IH_APP_URL}/confirm/")
    response = client.post(f"/api/user/confirm-email/{confirmation_code}")
    assert response.status_code == 204

    session.refresh(user)
    assert user.confirmation_code is None
    assert user.confirmed is True

    session.delete(user)
    session.commit()

def test_authenticated_register(admin_client: TestClient):
    registration = UserCreate(
        email="test@test.com",
        username="test",
        password="123456789",
        password_confirmation="123456789",
        first_name="Test",
        last_name="Test"
    )

    response = admin_client.post("/api/user/register/", json=registration.model_dump(by_alias=True))
    assert response.status_code == 403
    data = response.json()
    assert data["detail"] == "You are already logged in. If you want to create a new account, please logout first"

def test_register_password_check(client: TestClient):
    registration = UserCreate(
        email="test@test.com",
        username="test",
        password="1234567891",
        password_confirmation="123456789",
        first_name="Test",
        last_name="Test"
    )

    response = client.post("/api/user/register/", json=registration.model_dump(by_alias=True))
    assert response.status_code == 422
    assert response.json()["detail"] == "The given passwords do not match"