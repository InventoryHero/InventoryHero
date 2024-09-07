from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()
migrate = Migrate()


# TODO SQLALCHEMY REAL AUTOINCREMENT FEATURE
@migrate.configure
def configure_alembic(config):
    # modify config object
    return config
