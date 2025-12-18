import contextlib
import pytest
from fastapi.testclient import TestClient
from sqlmodel import cast
from ih.core.config import get_app_settings
from ih.app import app as real_app
from ih.core.settings.provider import SQLiteProvider

@pytest.fixture(scope="session")
def admin_client():
    client = TestClient(real_app)
    settings = get_app_settings()
    response = client.post("/api/auth/token", data={
        "username": settings._IH_DEFAULT_USERNAME,
        "password": settings._IH_DEFAULT_PASSWORD
    })
    assert response.status_code == 200

    yield client


    with contextlib.suppress(Exception):
        settings = get_app_settings()
        if settings.DB_PROVIDER is not None:
            sqlite_provider = cast(SQLiteProvider, settings.DB_PROVIDER)
            sqlite_provider.db_path.unlink()
