import os
from pathlib import Path
from alembic.config import Config
from alembic import command, config, script
from alembic.runtime import migration
from ih.db.db_setup import engine
from ih.db.models.User import User
from ih.core.security.password import hash_password
from ih.core.config import get_app_settings
from sqlmodel import Session, select

ALEMBIC_DIR = Path(__file__).resolve().parent.parent / "alembic"

def init_db():

    alembic_cfg_path = os.getenv("ALEMBIC_CONFIG_FILE", default=str(ALEMBIC_DIR / "alembic.ini"))
    alembic_cfg = Config(alembic_cfg_path)
    command.upgrade(alembic_cfg, "head")

    # initialize database with admin user
    settings = get_app_settings()
    with Session(engine) as session:
        existing = session.exec(select(User)).first()

        if existing is None:
            default_user = User(
                username=settings._IH_DEFAULT_USERNAME,
                email=settings._IH_DEFAULT_EMAIL,
                confirmed=True,
                password=hash_password(settings._IH_DEFAULT_PASSWORD),
                admin=True
            )
            session.add(default_user)
            session.commit()

        if not settings.PRODUCTION:
            # MAYBE ADD SOME MORE USERS HERE FOR DEVELOPMENT
            pass

if __name__ == "__main__":
    init_db()
