from pathlib import Path
import dotenv
import os
from functools import lru_cache

from ih.core.settings.settings import AppSettings, build_app_settings

CWD = Path(__file__).parent
BASE_DIR = CWD.parent.parent
ENV = BASE_DIR.joinpath(".env")

dotenv.load_dotenv(ENV)

PRODUCTION = os.getenv("PRODUCTION", "True").lower() in ["true", "1"]
TESTING = os.getenv("TESTING", "False").lower() in ["true", "1"]

DATA_DIR = os.getenv("DATA_DIR")



def get_data_dir() -> Path:
    global PRODUCTION, TESTING, DATA_DIR, BASE_DIR

    if TESTING:
        return BASE_DIR.joinpath("tests/.temp")

    if PRODUCTION:
        return Path(DATA_DIR if DATA_DIR else "/data")

    return BASE_DIR.joinpath("data")

@lru_cache()
def get_app_settings() -> AppSettings:
    return build_app_settings(ENV, get_data_dir())