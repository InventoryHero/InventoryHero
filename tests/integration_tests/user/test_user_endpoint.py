import hashlib

from fastapi.testclient import TestClient
from sqlmodel import Session, select
from bs4 import BeautifulSoup

from ih.core.config import get_app_settings
from ih.db.db_setup import engine
from ih.db.models.User import User
from tests.fixtures.mailpit import wait_for_messages, get_message


def test_get_user_details(client: TestClient, user):
    form_data = {"username": user.username, "password": "test1"}
    response = client.post("/api/auth/token", data=form_data)
    assert response.status_code == 200

    response = client.get("/api/user/self")
    assert response.status_code == 200

    assert response.json()["username"] == user.username
    assert response.json()["email"] == user.email
    assert response.json()["first_name"] == user.first_name
    assert response.json()["last_name"] == user.last_name
    assert response.json()["admin"] == user.admin




def test_create_user_admin(client: TestClient):
    settings = get_app_settings()
    user = User(
        username="test2",
        email="test2@test2.com",
        password="test2",
        admin=False
    )
    response = client.post("/api/auth/token", data={
        "username": settings._IH_DEFAULT_USERNAME,
        "password": settings._IH_DEFAULT_PASSWORD
    })
    assert response.status_code == 200
    assert "set-cookie" in response.headers

    response = client.post("/api/admin/user/create", json={
        "username": user.username,
        "email": user.email,
        "password": user.password,
        "admin": user.admin
    })
    assert response.status_code == 201
    assert response.json()["username"] == user.username
    assert response.json()["email"] == user.email
    assert response.json()["admin"] == user.admin

    # cleanup
    with Session(engine) as session:
        user = session.exec(select(User).where(User.username == user.username)).first()
        session.delete(user)
        session.commit()
        
def test_admin_get(client: TestClient, user):
    settings = get_app_settings()
    response = client.post("/api/auth/token", data={
        "username": settings._IH_DEFAULT_USERNAME,
        "password": settings._IH_DEFAULT_PASSWORD
    })
    assert response.status_code == 200
    assert "set-cookie" in response.headers

    response = client.get(f"/api/admin/user/{user.id}")
    assert response.status_code == 200
    data = response.json()
    assert data["email"] == user.email
    assert data["username"] == user.username


def test_delete_user_admin(authenticated_client: TestClient, user):
    settings = get_app_settings()
    response = authenticated_client.delete(f"/api/admin/user/{user.id}")
    assert response.status_code == 204

    response = authenticated_client.get(f"/api/admin/user/users")
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)
    assert len(data) == 1
    assert data[0]["username"] == settings._IH_DEFAULT_USERNAME

    response = authenticated_client.delete(f"/api/admin/user/{data[0]['id']}")
    assert response.status_code == 400
    data = response.json()
    assert data["detail"] == {'message': 'Deleting your own account is not supported from here', 'toast': True, 'toast_type': 'error'}

def test_admin_user_update(authenticated_client: TestClient, user):
    response = authenticated_client.put(f"/api/admin/user/{user.id}", json={
        "first_name": "xx",
        "last_name": "xx",
        "email": "xx@xx.xx",
        "username": "yyy",
        "admin": True
    })
    assert response.status_code == 200
    data = response.json()
    assert data["first_name"] == "xx"
    assert data["last_name"] == "xx"
    assert data["username"] == "yyy"
    assert data["email"] == "xx@xx.xx"
    assert data["admin"]

    # test updating nonexisting user
    response = authenticated_client.put(f"/api/admin/user/0f96397f-d636-4afa-860c-7b0af864ab0f", json={
        "first_name": "yy"
    })
    assert response.status_code == 404

def test_admin_user_reset_password(authenticated_client: TestClient, user, session):
    settings = get_app_settings()
    response = authenticated_client.put(f"/api/admin/user/{user.id}/reset-password")
    assert response.status_code == 200
    assert response.json().startswith(f"{settings.IH_APP_URL}/password-reset/")

    messages = wait_for_messages()
    assert messages["total"] == 1

    msg = messages["messages"][0]
    assert msg["To"][0]["Address"] == user.email
    assert "password" in msg["Subject"].lower()

    body = get_message(msg["ID"])
    assert f"{settings.IH_APP_URL}/password-reset/" in body["HTML"]

    soup = BeautifulSoup(body["HTML"], "html.parser")
    reset_links = [
        link for link in [a["href"] for a in soup.find_all("a", href=True)]
        if "/password-reset/" in link
    ]
    assert len(reset_links) == 2
    assert reset_links[0] == reset_links[1]

    session.refresh(user)
    code = reset_links[0].split("/")[-1]
    code = hashlib.sha256(code.encode()).hexdigest()

    assert user.password_reset_token == code

    response = authenticated_client.put(f"/api/admin/user/0f96397f-d636-4afa-860c-7b0af864ab0f/password-reset")
    assert response.status_code == 404
    
def test_admin_resend_confirmation(authenticated_client: TestClient, user, monkeypatch):

    get_app_settings.cache_clear()
    settings = get_app_settings()
    assert settings.IH_SMTP_ENABLED

    response = authenticated_client.post(f"/api/admin/user/{user.id}/resend-confirmation")
    assert response.status_code == 204

    # confirm email validity
    messages = wait_for_messages()
    assert messages["total"] == 1
    msg = messages["messages"][0]
    assert msg["To"][0]["Address"] == user.email
    assert "confirm your e-mail" == msg["Subject"].lower()
    body = get_message(msg["ID"])
    assert f"{settings.IH_APP_URL}/confirm/" in body["HTML"]

    response = authenticated_client.post(f"/api/admin/user/0f96397f-d636-4afa-860c-7b0af864ab0f/resend-confirmation")
    assert response.status_code == 404
    assert response.json()["detail"] == "The requested user does not exist"

    # disable email
    monkeypatch.setenv("IH_SMTP_HOST", "")
    get_app_settings.cache_clear()
    settings = get_app_settings()
    assert not settings.IH_SMTP_ENABLED

    response = authenticated_client.post(f"/api/admin/user/{user.id}/resend-confirmation")
    assert response.status_code == 400
    assert response.json()["detail"]["message"] == "SMTP is disabled, cannot send emails"




