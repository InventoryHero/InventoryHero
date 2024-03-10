from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()
migrate = Migrate()


@migrate.configure
def configure_alembic(config):
    # modify config object
    return config
