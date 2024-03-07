import os, logging
from flask_socketio import SocketIO
from flask import Flask
from flask_jwt_extended import JWTManager
from flask_cors import CORS

from database import db
from datetime import timedelta




class Config(object):
    SQLALCHEMY_DATABASE_URI = \
        os.getenv("DATABASE_URI", "") or os.getenv("DATABASE_CONNECTION", "") or "sqlite:///:memory:"


    # TODO CHECK IF FILE EXISTS / CREATE FILE

    if SQLALCHEMY_DATABASE_URI.startswith("sqlite"):
        SQLALCHEMY_DATABASE_URI = SQLALCHEMY_DATABASE_URI.replace("sqlite", "sqlite+pysqlite")

    SECRET_KEY = os.getenv("JWT_SECRET_KEY", "SUPER_SECRET_KEY")

    JWT_ACCESS_TOKEN_EXPIRES = timedelta(minutes=int(os.getenv("JWT_ACCESS_TOKEN_EXPIRES", "60")))
    JWT_REFRESH_TOKEN_EXPIRES = timedelta(days=int(os.getenv("JWT_REFRESH_TOKEN_EXPIRES", "30")))

    SMTP = {
        "server": os.getenv("SMTP_SERVER", None),
        "port": os.getenv("SMTP_PORT", None),
        "username": os.getenv("SMTP_USERNAME", None),
        "password": os.getenv("SMTP_PASSWORD", None),
        "sender_email": os.getenv("SMTP_EMAIL_ADDRESS", "noreply@inventory-hero.local"),
        "in_use": False
    }

    SMTP["in_use"] = (SMTP["server"] is not None and SMTP["port"] is not None
                             and SMTP["password"] is not None and SMTP["username"] is not None)

    CONFIRMATION_NEEDED = os.getenv("CONFIRMATION_NEEDED", "False").lower() in ('true', '1', 't')

    if CONFIRMATION_NEEDED and not SMTP["in_use"]:
        raise Exception("ENTER SMTP CONFIG OR DISABLE CONFIRMATION")

    APP_URL = os.getenv("APP_URL", "http://localhost:3000")


class DebugConfig(Config):
    FLASK_DEBUG = True


class ProdConfig(Config):
    FLASK_DEBUG = False


def get_config():
    is_development = os.getenv("IS_DEVELOPMENT", "True").lower() in ('true', '1', 't')
    if is_development:
        return DebugConfig
    return ProdConfig


app = Flask(__name__)
app.config.from_object(get_config())
app.logger.error(app.config)
jwt = JWTManager(app)

db.init_app(app)
gunicorn_logger = logging.getLogger('gunicorn.error')
app.logger.handlers.extend(gunicorn_logger.handlers)
app.logger.setLevel(logging.INFO)
CORS(app, origins=["*"])
socketio = SocketIO(app, cors_allowed_origins="*")
