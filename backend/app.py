import os

from dotenv import load_dotenv
import flask_migrate
from flask import jsonify

from backend.endpoints.User import User
from backend.endpoints.ProductEndpoint import ProductEndpoint
from backend.endpoints.StorageEndpoint import StorageEndpoint
from backend.endpoints.HouseholdEndpoint import HouseholdEndpoint

from backend.flask_config import app, socketio
from backend.sockets.sockets import HouseholdSocket, GeneralSocket
from backend.database import db, migrate
from backend.endpoints.AdminEndpoint import AdminEndpoint


load_dotenv()

url_prefix = "/api/v1/<int:household>"
user = User('user', __name__, application=app, db=db, url_prefix="/api/v1")
products = ProductEndpoint('product_endpoint', __name__, application=app, db=db, url_prefix=url_prefix)
storage = StorageEndpoint('storage_endpoint', __name__, application=app, db=db, url_prefix=url_prefix)
household = HouseholdEndpoint('household_endpoint', __name__, application=app, db=db, url_prefix="/api/v1")
admin = AdminEndpoint('admin_endpoint', __name__, application=app, db=db, url_prefix="/api/v1")
app.register_blueprint(user)
app.register_blueprint(products)
app.register_blueprint(storage)
app.register_blueprint(household)
app.register_blueprint(admin)

socketio.on_namespace(HouseholdSocket("/household"))
socketio.on_namespace(GeneralSocket("/general"))


@app.route("/api/v1/smtp-enabled")
def check_smtp():
    app.logger.info(app.config['SMTP'].values())
    smtp_configured = all(app.config['SMTP'].values())
    return jsonify(enabled=smtp_configured), 200


if __name__ == "__main__":
    port = int(os.environ.get('PORT', 5000))
    socketio.run(app, port=port, host="0.0.0.0")
