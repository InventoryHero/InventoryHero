import datetime
import hashlib

from fastapi.testclient import TestClient
from sqlmodel import Session, select
from bs4 import BeautifulSoup

from ih.core.config import get_app_settings
from ih.core.security.password import hash_password, verify_password
from ih.core.security.provider import AuthenticationProvider
from ih.db.db_setup import engine
from ih.db.models import Household, HouseholdMember
from ih.db.models.User import User
from ih.schema.households import Role, HouseholdWithMemberPublic
from tests.utils.email import wait_for_messages, get_message, parse_email_messages, assert_no_messages, clear_messages


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


def test_delete_user_admin(admin_client: TestClient, user):
    settings = get_app_settings()
    response = admin_client.delete(f"/api/admin/user/{user.id}")
    assert response.status_code == 204

    response = admin_client.get(f"/api/admin/user/users")
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)
    assert len(data) == 1
    assert data[0]["username"] == settings._IH_DEFAULT_USERNAME

    response = admin_client.delete(f"/api/admin/user/{data[0]['id']}")
    assert response.status_code == 400
    data = response.json()
    assert data["detail"] == {'message': 'Deleting your own account is not supported from here', 'toast': True, 'toast_type': 'error'}

def test_admin_user_update(admin_client: TestClient, user):
    response = admin_client.put(f"/api/admin/user/{user.id}", json={
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
    response = admin_client.put(f"/api/admin/user/0f96397f-d636-4afa-860c-7b0af864ab0f", json={
        "first_name": "yy"
    })
    assert response.status_code == 404

def test_admin_user_reset_password(admin_client: TestClient, user, session):
    settings = get_app_settings()
    response = admin_client.put(f"/api/admin/user/{user.id}/reset-password")
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

    response = admin_client.put(f"/api/admin/user/0f96397f-0000-4afa-860c-7b0af864ab0f/password-reset")
    assert response.status_code == 404
    
def test_admin_resend_confirmation(admin_client: TestClient, user, monkeypatch):

    get_app_settings.cache_clear()
    settings = get_app_settings()
    assert settings.IH_SMTP_ENABLED

    response = admin_client.post(f"/api/admin/user/{user.id}/resend-confirmation")
    assert response.status_code == 204

    # confirm email validity
    messages = wait_for_messages()
    assert messages["total"] == 1
    msg = messages["messages"][0]
    assert msg["To"][0]["Address"] == user.email
    assert "confirm your e-mail" == msg["Subject"].lower()
    body = get_message(msg["ID"])
    assert f"{settings.IH_APP_URL}/confirm/" in body["HTML"]

    response = admin_client.post(f"/api/admin/user/0f96397f-d636-4afa-860c-7b0af864ab0f/resend-confirmation")
    assert response.status_code == 404
    assert response.json()["detail"] == "The requested user does not exist"

    # disable email
    monkeypatch.setenv("IH_SMTP_HOST", "")
    get_app_settings.cache_clear()
    settings = get_app_settings()
    assert not settings.IH_SMTP_ENABLED

    response = admin_client.post(f"/api/admin/user/{user.id}/resend-confirmation")
    assert response.status_code == 400
    assert response.json()["detail"]["message"] == "SMTP is disabled, cannot send emails"

    #reenable SMTP
    monkeypatch.setenv("IH_SMTP_HOST", "localhost")
    get_app_settings.cache_clear()

def test_user_reset_password(client: TestClient, user, session):
    settings = get_app_settings()

    # request password reset
    response = client.post(
        "/api/user/reset-password",
        json={"email": user.email},
    )
    assert response.status_code == 204
    assert response.content == b""

    # wait for email to arrive in Mailpit
    messages = wait_for_messages()
    assert messages["total"] == 1

    msg = messages["messages"][0]
    assert msg["To"][0]["Address"] == user.email
    assert "password" in msg["Subject"].lower()

    # fetch email body
    body = get_message(msg["ID"])
    assert f"{settings.IH_APP_URL}/password-reset/" in body["HTML"]

    # extract reset links
    soup = BeautifulSoup(body["HTML"], "html.parser")
    reset_links = [
        a["href"]
        for a in soup.find_all("a", href=True)
        if "/password-reset/" in a["href"]
    ]

    assert len(reset_links) == 2
    assert reset_links[0] == reset_links[1]

    # verify token stored in DB matches email link
    session.refresh(user)
    raw_code = reset_links[0].split("/")[-1]
    hashed_code = hashlib.sha256(raw_code.encode()).hexdigest()

    assert user.password_reset_token == hashed_code

def test_validate_password_reset_token(client: TestClient, user, session):
    # 1. Request password reset (issue token)
    response = client.post(
        "/api/user/reset-password",
        json={"email": user.email},
    )
    assert response.status_code == 204

    # 2. Read reset email
    messages = wait_for_messages()
    assert messages["total"] == 1

    msg = messages["messages"][0]
    body = get_message(msg["ID"])

    soup = BeautifulSoup(body["HTML"], "html.parser")
    reset_link = next(
        a["href"]
        for a in soup.find_all("a", href=True)
        if "/password-reset/" in a["href"]
    )

    raw_code = reset_link.split("/")[-1]
    assert raw_code  # sanity check

    # 3. Validate token
    response = client.get(f"/api/user/validate-password-token/{raw_code}")
    assert response.status_code == 200

    data = response.json()
    assert data["valid"] is True
    assert data["reason"] is None

    session.refresh(user)
    user.password_reset_token_expires_at = datetime.datetime.now(datetime.timezone.utc) - datetime.timedelta(minutes=1)
    session.commit()

    response = client.get(f"/api/user/validate-password-token/{raw_code}")
    assert response.status_code == 200

    data = response.json()
    assert data["valid"] is False
    assert data["reason"] == "The token is invalid, please request a new one!"

    response = client.get(f"/api/user/validate-password-token/this-code-is-invalid")
    assert response.status_code == 200

    data = response.json()
    assert data["valid"] is False
    assert data["reason"] == "The token is invalid, please request a new one!"

def test_user_reset_password_with_code(client: TestClient, user, session):
    response = client.post(
        "/api/user/reset-password",
        json={"email": user.email},
    )
    assert response.status_code == 204

    messages = wait_for_messages()
    assert messages["total"] == 1

    msg = messages["messages"][0]
    body = get_message(msg["ID"])

    soup = BeautifulSoup(body["HTML"], "html.parser")
    reset_link = next(
        a["href"]
        for a in soup.find_all("a", href=True)
        if "/password-reset/" in a["href"]
    )
    raw_code = reset_link.split("/")[-1]
    new_password = "NewStrongPassword123!"

    session.refresh(user)
    user.password_reset_token_expires_at = datetime.datetime.now(datetime.timezone.utc) - datetime.timedelta(minutes=1)
    session.commit()
    response = client.post(
        f"/api/user/reset-password/{raw_code}",
        json={"new_password": new_password, "new_password_confirmation": new_password},
    )
    assert response.status_code == 200
    data = response.json()
    assert data["valid"] is False
    assert data["reason"] == "The token is invalid, please request a new one!"

    response = client.post(
        f"/api/user/reset-password/this-code-is-invalid",
        json={"new_password": new_password, "new_password_confirmation": new_password},
    )
    assert response.status_code == 200
    data = response.json()
    assert data["valid"] is False
    assert data["reason"] == "The token is invalid, please request a new one!"

    session.refresh(user)
    user.password_reset_token_expires_at = datetime.datetime.now(datetime.timezone.utc) + datetime.timedelta(minutes=1)
    session.commit()
    response = client.post(
        f"/api/user/reset-password/{raw_code}",
        json={"new_password": new_password, "new_password_confirmation": "not-equal"},
    )
    assert response.status_code == 400
    data = response.json()["detail"]
    assert data["toast"] is True
    assert data["message"] == "The given passwords do not match"
    session.refresh(user)
    assert user.password_reset_token is not None
    assert user.password_reset_token_expires_at is not None


    response = client.post(
        f"/api/user/reset-password/{raw_code}",
        json={"new_password": new_password, "new_password_confirmation": new_password},
    )
    assert response.status_code == 200
    data = response.json()
    assert data["valid"] is True
    assert data["reason"] is None
    session.refresh(user)
    assert user.password_reset_token is None
    assert user.password_reset_token_expires_at is None
    assert verify_password(new_password,user.password)

def test_get_current_household(admin_client: TestClient, user, session):
    response = admin_client.get("/api/user/current-household")
    assert response.status_code == 200
    assert response.content == b'null'

def test_set_current_household(admin_client: TestClient, session):
    response = admin_client.post("/api/user/current-household",json={"id": '00000000-0000-0000-0000-000000000000'},)
    assert response.status_code == 404
    assert response.json()["detail"] == "Household not found"

    settings = get_app_settings()
    user  = session.exec(select(User).where(User.username == settings._IH_DEFAULT_USERNAME)).first()
    assert user

    household = Household(name="test")
    session.add(household)
    session.flush()
    session.refresh(household)

    household_member = HouseholdMember(user_id = user.id, household_id = household.id, role = Role.OWNER)
    session.add(household_member)
    session.commit()
    session.refresh(household_member)

    response = admin_client.post("/api/user/current-household", json={"id": str(household.id)} )
    assert response.status_code == 200
    default_household: HouseholdWithMemberPublic = HouseholdWithMemberPublic(**response.json())
    assert default_household.id == household.id
    assert default_household.name == household.name
    assert default_household.member.user_id == user.id
    assert default_household.member.role == Role.OWNER

    response = admin_client.get("/api/user/current-household")
    assert response.status_code == 200
    default_household: HouseholdWithMemberPublic = HouseholdWithMemberPublic(**response.json())
    assert default_household.id == household.id
    assert default_household.name == household.name
    assert default_household.member.user_id == user.id
    assert default_household.member.role == Role.OWNER

    session.delete(household)
    session.commit()

    assert len(session.exec(select(HouseholdMember)).all()) == 0

    response = admin_client.get("/api/user/current-household")
    assert response.status_code == 200
    assert response.content == b'null'

def test_change_password(client: TestClient, user, session):
    response = client.post("/api/auth/token", data={
        "username": user.username,
        "password": "test1"
    })
    assert response.status_code == 200

    response = client.post("/api/user/change-password", json={"current_password": "test1", "new_password": "test1234", "new_password_confirmation": "test1234"})
    assert response.status_code == 204

    session.refresh(user)
    assert verify_password("test1234", user.password)

    response = client.post("/api/user/change-password", json={"current_password": "test1234", "new_password": "test11",
                                                              "new_password_confirmation": "test1"})
    assert response.status_code == 422
    data = response.json()["detail"]
    assert data["message"] == "The given passwords do not match"

    response = client.post("/api/user/change-password", json={"current_password": "test1", "new_password": "test1",
                                                              "new_password_confirmation": "test1"})
    assert response.status_code == 403
    data = response.json()["detail"]
    assert data["message"] == "wrong_password"
    assert data["toast"] is False

    response = client.post("/api/user/change-password", json={"current_password": "test1234", "new_password": "test1",
                                                              "new_password_confirmation": "test1"})
    assert response.status_code == 204

def test_update_user(client: TestClient, user, session, monkeypatch):

    settings = get_app_settings()
    assert settings.IH_SMTP_ENABLED
    response = client.post("/api/auth/token", data={
        "username": user.username,
        "password": "test1"
    })
    assert response.status_code == 200

    response = client.put("/api/user/self", json={
        "username": "test2",
        "email": "test2@test2.com",
        "first_name": "new_firstname",
        "last_name": "new_lastname",
    })

    assert response.status_code == 200
    updated = response.json()
    assert updated["username"] == "test2"
    assert updated["email"] == "test2@test2.com"
    assert updated["first_name"] == "new_firstname"
    assert updated["last_name"] == "new_lastname"
    assert updated["admin"] is False

    session.refresh(user)
    assert user.confirmation_code is not None
    assert user.confirmed is False
    parse_email_messages("test2@test2.com", f"{settings.IH_APP_URL}/confirm/")
    clear_messages()
    user.confirmation_code = None
    user.confirmed = True
    session.commit()


    response = client.put("/api/user/self", json={
        "username": settings._IH_DEFAULT_USERNAME,
        "first_name": "old_firstname"
    })
    assert response.status_code == 500
    session.refresh(user)
    assert user.username == "test2"
    assert user.first_name == "new_firstname"

    response = client.put("/api/user/self", json={})
    assert response.status_code == 200
    updated = response.json()
    session.refresh(user)
    assert updated["username"] == "test2"
    assert updated["email"] == "test2@test2.com"
    assert updated["first_name"] == "new_firstname"
    assert updated["last_name"] == "new_lastname"
    assert updated["admin"] is False

    response = client.put("/api/user/self", json={
        "email": settings._IH_DEFAULT_EMAIL,
        "first_name": "old_firstname"
    })
    assert response.status_code == 500
    session.refresh(user)
    assert updated["email"] == "test2@test2.com"
    assert user.first_name == "new_firstname"

    assert user.confirmation_code is None
    assert user.confirmed is True
    assert_no_messages()

    response = client.put("/api/user/self", json={
        "username": "test2",
        "email": "test2@test2.com",
        "first_name": "new_firstname",
        "last_name": "new_lastname",
    })
    assert response.status_code == 200
    updated = response.json()
    session.refresh(user)
    assert updated["username"] == "test2"
    assert updated["email"] == "test2@test2.com"
    assert updated["first_name"] == "new_firstname"
    assert updated["last_name"] == "new_lastname"
    assert updated["admin"] is False
    assert_no_messages()

    monkeypatch.setenv("IH_SMTP_HOST", "")
    get_app_settings.cache_clear()
    response = client.put("/api/user/self", json={
        "email": "test3@test3.com",
    })
    assert response.status_code == 200
    updated = response.json()
    session.refresh(user)
    assert updated["username"] == "test2"
    assert updated["email"] == "test3@test3.com"
    assert updated["first_name"] == "new_firstname"
    assert updated["last_name"] == "new_lastname"
    assert updated["admin"] is False
    assert_no_messages()

    monkeypatch.setenv("IH_SMTP_HOST", "localhost")
    get_app_settings.cache_clear()



