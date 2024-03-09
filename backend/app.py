import os

from database import db
from endpoints.User import User
from endpoints.ProductEndpoint import ProductEndpoint
from endpoints.StorageEndpoint import StorageEndpoint
from endpoints.HouseholdEndpoint import HouseholdEndpoint

from flask_config import app, socketio
from sockets.sockets import HouseholdSocket

from dotenv import load_dotenv

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



socketio.on_namespace(HouseholdSocket("/household"))

if __name__ == "__main__":
    port = int(os.environ.get('PORT', 5000))
    with app.app_context():
        db.create_all()
    socketio.run(app, port=port, host="0.0.0.0")
else:
    with app.app_context():
        db.create_all()
