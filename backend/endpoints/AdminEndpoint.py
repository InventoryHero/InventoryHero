from functools import wraps

from flask import Blueprint, jsonify
from flask_jwt_extended import jwt_required, current_user

from backend.db.models.User import User


def require_admin(f):
    @wraps(f)
    def decorator(*args, **kwargs):
        if not current_user.is_admin:
            return jsonify(), 403
        return f(*args, **kwargs)
    return decorator


class AdminEndpoint(Blueprint):
    def __init__(self, name, import_name, application, db, url_prefix, *args):
        self.app = application
        self.db = db

        url_prefix += ("" if url_prefix.endswith("/") else "/") + "administration"

        super(AdminEndpoint, self).__init__(name=name, import_name=import_name, url_prefix=url_prefix, *args)

        @self.route("/users", methods=["GET"])
        @jwt_required()
        @require_admin
        def get_users():
            users = User.query.all()
            users = [user.serialize() for user in users]
            return jsonify(users=users), 200
