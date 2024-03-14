import os
import sys

import bcrypt

from backend.db.models.User import User
from backend.flask_config import app, db
from exceptions.inventory_hero_exceptions import UserExistsButNoAdmin


def create_admin():
    with app.app_context():
        username = os.getenv("INVENTORYHERO_ADMIN_USERNAME", "admin")
        email = os.getenv("INVENTORYHERO_ADMIN_EMAIL", "admin@inventory.hero")
        password = os.getenv("INVENTORYHERO_ADMIN_PASSWORD", "changeme")

        existing_user = db.session.query(User).filter_by(username=username).first()
        if existing_user and not existing_user.is_admin:
            raise UserExistsButNoAdmin("A user with this username already exists but is not an administrator.")

        if not db.session.query(User).filter_by(is_admin=True).first():
            password = password.encode('utf-8')
            salt = bcrypt.gensalt()
            password = bcrypt.hashpw(password, salt)
            user = User(
                username=username,
                email=email,
                password=password.decode("utf-8"),
                email_confirmed=True,
                is_admin=True
            )
            db.session.add(user)
            db.session.commit()
            db.close_all_sessions()


if __name__ == "__main__":
    try:
        create_admin()
    except UserExistsButNoAdmin as e:
        print(e)
        sys.exit(1)
