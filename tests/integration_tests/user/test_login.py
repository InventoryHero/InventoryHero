import pytest
from fastapi.testclient import TestClient
from ih.core.config import get_app_settings


def test_login_fail(client: TestClient, monkeypatch):
    settings = get_app_settings()
    form_data = {"username": settings._IH_DEFAULT_USERNAME, "password": "something"}
    response = client.post("/api/auth/token", data=form_data)
    assert response.status_code == 401



@pytest.mark.usefixtures("user")
def test_login(request: pytest.FixtureRequest, client: TestClient, monkeypatch):
    settings = get_app_settings()
    print(settings.DB_PROVIDER.db_url)
    form_data = {"username": settings._IH_DEFAULT_USERNAME, "password": settings._IH_DEFAULT_PASSWORD}
    response = client.post("/api/auth/token", data=form_data)
    assert response.status_code == 200
    assert "set-cookie" in response.headers

    response = client.get("/api/user/self")
    assert response.status_code == 200
    assert response.json()["username"] == settings._IH_DEFAULT_USERNAME


    user = request.getfixturevalue("user")
    form_data = {"username": user.username, "password": "test1"}
    response = client.post("/api/auth/token", data=form_data)
    assert response.status_code == 200