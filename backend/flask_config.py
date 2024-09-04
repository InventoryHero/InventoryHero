import os, logging
from flask_socketio import SocketIO
from flask import Flask
from flask_jwt_extended import JWTManager
from flask_cors import CORS

from backend.database import db, migrate
from datetime import timedelta


from backend.exceptions.inventory_hero_exceptions import UnknownDatabaseType, MissingSmtpConfig, InvalidAppUrl, \
    UnsupportedSmtpProtocol


def parse_db_parameters(db_type, db_host, db_port, db_name, db_user, db_password):
    logger = logging.getLogger('config')
    if db_type != "sqlite" and any(param is None for param in [db_host, db_port, db_name, db_user, db_password]):
        logger.warning(f"Invalid database parameters for type {db_type}. Using sqlite as a default.")
        db_type = "sqlite"

    if db_type == "sqlite":
        driver = "sqlite+pysqlite"
        file_path = ""
        logger.warning(os.getcwd())
        if os.path.exists("../data"):
            file_path = "/../data/inventoryhero.db"
        else:
            logger.warning("../data/inventoryhero.db not found, using memory based sqlite instance.")

        db_uri = f"{driver}://{file_path}"
    elif db_type == "mysql":
        driver = "mysql+mysqldb"
        db_uri = f"{driver}://{db_user}:{db_password}@{db_host}:{db_port}/{db_name}"
    elif db_type == "postgresql":
        driver = "postgresql+psycopg2"
        db_uri = f"{driver}://{db_user}:{db_password}@{db_host}:{db_port}/{db_name}"
    else:
        raise UnknownDatabaseType()
    return db_uri


class Config(object):
    logger = logging.getLogger('config')
    DB_TYPE = os.getenv('INVENTORYHERO_DB_TYPE', "sqlite")
    DB_HOST = os.getenv('INVENTORYHERO_DB_HOST', None)
    DB_PORT = os.getenv('INVENTORYHERO_DB_PORT', None)
    DB_NAME = os.getenv('INVENTORYHERO_DB_NAME', None)
    DB_USER = os.getenv('INVENTORYHERO_DB_USER', None)
    DB_PASSWORD = os.getenv('INVENTORYHERO_DB_PASSWORD', None)

    SQLALCHEMY_DATABASE_URI = parse_db_parameters(DB_TYPE, DB_HOST, DB_PORT, DB_NAME, DB_USER, DB_PASSWORD)

    SECRET_KEY = os.getenv("INVENTORYHERO_SECRET_KEY", "SUPER_SECRET_KEY")

    JWT_ACCESS_TOKEN_EXPIRES = timedelta(minutes=60)
    JWT_REFRESH_TOKEN_EXPIRES = timedelta(days=30)
    JWT_TOKEN_LOCATION = ["headers"]

    SMTP = {
        "server": os.getenv("INVENTORYHERO_SMTP_SERVER", None),
        "port": os.getenv("INVENTORYHERO_SMTP_PORT", None),
        "protocol": os.getenv("INVENTORYHERO_SMTP_PROTOCOL", "SSL"),
        "username": os.getenv("INVENTORYHERO_SMTP_USERNAME", None),
        "password": os.getenv("INVENTORYHERO_SMTP_PASSWORD", None),
        "from_email": os.getenv("INVENTORYHERO_SMTP_FROM_ADDRESS", "noreply@inventory-hero.local"),
        "from_name": os.getenv("INVENTORYHERO_SMTP_FROM_NAME", "InventoryHero"),
        "in_use": False
    }

    if SMTP["protocol"] != "SSL":
        raise UnsupportedSmtpProtocol()

    SMTP["in_use"] = (SMTP["server"] is not None and SMTP["port"] is not None
                      and SMTP["password"] is not None and SMTP["username"] is not None)

    CONFIRMATION_NEEDED = os.getenv("INVENTORYHERO_CONFIRMATION_NEEDED", "false").lower() in ('true', '1', 't')

    if CONFIRMATION_NEEDED and not SMTP["in_use"]:
        raise MissingSmtpConfig("ENTER SMTP CONFIG OR DISABLE CONFIRMATION")

    APP_URL = os.getenv("INVENTORYHERO_APP_URL", "http://localhost:8080")

    REGISTRATION_ALLOWED = os.getenv("INVENTORYHERO_REGISTRATION_ALLOWED", "true").lower() in ('true', '1', 't')

    


class DebugConfig(Config):
    DEBUG = True
    TESTING = True
    ALLOWED_ORIGINS = ["https://localhost:3000", "http://localhost:3000"]


class ProdConfig(Config):
    DEBUG = False
    TESTING = False
    ALLOWED_ORIGINS = [Config.APP_URL]


def get_config():
    is_development = os.getenv("IS_DEVELOPMENT", "true").lower() in ('true', '1', 't')
    if is_development:
        return DebugConfig
    return ProdConfig


app = Flask(__name__)
app.config.from_object(get_config())
app.logger.error(app.config)
jwt = JWTManager(app)


socketio = SocketIO(app, cors_allowed_origins=app.config["ALLOWED_ORIGINS"])
gunicorn_logger = logging.getLogger('gunicorn.error')
app.logger.handlers.extend(gunicorn_logger.handlers)
app.logger.setLevel(logging.INFO)
CORS(app, origins=app.config["ALLOWED_ORIGINS"])

from backend.db.models import PasswordResetRequests
db.init_app(app)
migrate.init_app(app, db, render_as_batch=True)


