import os

from dotenv import load_dotenv
import flask_migrate

from backend.endpoints.User import User
from backend.endpoints.ProductEndpoint import ProductEndpoint
from backend.endpoints.StorageEndpoint import StorageEndpoint
from backend.endpoints.HouseholdEndpoint import HouseholdEndpoint

from backend.flask_config import app, socketio
from backend.sockets.sockets import HouseholdSocket
from backend.database import db, migrate

load_dotenv()

url_prefix = "/api/v1/<int:household>"
user = User('user', __name__, application=app, db=db, url_prefix="/api/v1")
products = ProductEndpoint('product_endpoint', __name__, application=app, db=db, url_prefix=url_prefix)
storage = StorageEndpoint('storage_endpoint', __name__, application=app, db=db, url_prefix=url_prefix)
household = HouseholdEndpoint('household_endpoint', __name__, application=app, db=db, url_prefix="/api/v1")
app.register_blueprint(user)
app.register_blueprint(products)
app.register_blueprint(storage)
app.register_blueprint(household)


def setup_app():
    db.init_app(app)
    migrate.init_app(app, db)
    socketio.on_namespace(HouseholdSocket("/household"))
    with app.app_context():
        db.create_all()
        flask_migrate.migrate()
        flask_migrate.upgrade()


if __name__ == "__main__":
    port = int(os.environ.get('PORT', 5000))
    setup_app()
    socketio.run(app, port=port, host="0.0.0.0")
else:
    setup_app()
