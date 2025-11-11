
from fastapi.testclient import TestClient
from sqlmodel import Session, select

from ih.core.config import get_app_settings
from ih.db.db_setup import engine
from ih.db.models.User import User


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

def test_admin_user_reset_password(authenticated_client: TestClient, user):
    settings = get_app_settings()
    response = authenticated_client.put(f"/api/admin/user/{user.id}/reset-password")
    assert response.status_code == 200
    assert response.json().startswith(f"{settings.IH_APP_URL}/password-reset/")
    
    response = authenticated_client.put(f"/api/admin/user/0f96397f-d636-4afa-860c-7b0af864ab0f/password-reset")
    assert response.status_code == 404

