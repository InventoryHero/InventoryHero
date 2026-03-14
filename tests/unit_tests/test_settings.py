import pytest
from dotenv import load_dotenv

from ih.core.config import get_app_settings


def test_default_database(monkeypatch):
    get_app_settings.cache_clear()
    app_settings = get_app_settings()

    assert app_settings.DB_URL.startswith("sqlite://") and app_settings.DB_URL.endswith("inventoryhero.db")

def test_postgres_database(monkeypatch):
    monkeypatch.setenv("IH_DB_ENGINE", "postgres")
    get_app_settings.cache_clear()
    app_settings = get_app_settings()
    assert app_settings.DB_URL == "postgresql://inventoryhero:inventoryhero@postgres:5432/inventoryhero"