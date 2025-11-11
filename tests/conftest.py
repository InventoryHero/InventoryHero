import contextlib
from pathlib import Path
from typing import cast, Generator
from pytest import MonkeyPatch, fixture


mp = MonkeyPatch()
mp.setenv("PRODUCTION", "False")
mp.setenv("TESTING", "True")
mp.setenv("IH_REGISTRATION_ALLOWED", "True")
mp.setenv("IH_SECRET_KEY", "supersecretteststring")
mp.setenv("IH_ACCESS_TOKEN_EXPIRATION", f"{3600*4}")

from fastapi.testclient import TestClient
from ih.db.init_db import init_db
from ih.app import app as real_app
from ih.core import config
from ih.core.settings.provider import SQLiteProvider
#from tests.fixtures.users import user
from tests.fixtures import *

init_db()



@fixture(scope="session")
def client():

    yield TestClient(real_app)

    # this deletes the inventoryhero.db
    with contextlib.suppress(Exception):
        settings = config.get_app_settings()
        if settings.DB_PROVIDER is not None:
            sqlite_provider = cast(SQLiteProvider, settings.DB_PROVIDER)
            sqlite_provider.db_path.unlink()


@fixture(scope="session", autouse=True)
def cleanup() -> Generator[None, None, None]:
    yield None

    temp_dir = Path(__file__).parent / ".temp"
    if not temp_dir.exists():
        return
    import shutil
    shutil.rmtree(temp_dir, ignore_errors=True)
