import uuid
from functools import wraps

from flask import Blueprint, jsonify
from flask_jwt_extended import jwt_required, current_user

from backend.db.models.User import User
from backend.mail.Mail import Mail


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

        @self.route("/resend/<int:user_id>", methods=["GET"])
        @jwt_required()
        @require_admin
        def resend_confirmation(user_id):
            user = User.query.filter_by(id=user_id).first()
            if user is None:
                return jsonify(status="user_not_found"), 422
            if user.email_confirmed:
                return jsonify(status="account_already_confirmed"), 400
            confirmation_code = None
            if self.app.config["CONFIRMATION_NEEDED"]:
                confirmation_code = uuid.uuid4()
            user.confirmation_code = confirmation_code
            if self.app.config["CONFIRMATION_NEEDED"]:
                mail = Mail(self.app.config["SMTP"], self.app.config["APP_URL"])
                mail.send_registration_confirmation(user.email, confirmation_code)
            self.db.session.commit()
            return jsonify(status="success"), 200

        @self.route("/reset-password/<int:user_id>", methods=["POST"])
        @jwt_required()
        @require_admin
        def reset_password(user_id):
            return jsonify(status=user_id), 422