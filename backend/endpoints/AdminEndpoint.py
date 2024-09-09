import uuid
from functools import wraps

import bcrypt
from flask import Blueprint, jsonify, request
from flask_jwt_extended import jwt_required, current_user

from backend.db.models.User import User
from backend.mail.Mail import Mail
from decorators import admin_required

class AdminEndpoint(Blueprint):
    def __init__(self, name, import_name, application, db, url_prefix, *args):
        self.app = application
        self.db = db

        url_prefix += ("" if url_prefix.endswith("/") else "/") + "administration"

        super(AdminEndpoint, self).__init__(name=name, import_name=import_name, url_prefix=url_prefix, *args)

        @self.route("/users", methods=["GET"])
        @jwt_required()
        @admin_required()
        def get_users():
            users = User.query.all()
            return jsonify(users=users), 200

        @self.route("/resend/<int:user_id>", methods=["GET"])
        @jwt_required()
        @admin_required()
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
        @admin_required()
        def reset_password(user_id):
            password = request.json.get('password', None)
            self.app.logger.info(f"Resetting password for user {user_id}: {password}")
            salt = bcrypt.gensalt()
            password = password.encode('utf-8')
            password = bcrypt.hashpw(password, salt)
            user = User.query.filter_by(id=user_id).first()
            if user is None:
                return jsonify(status="user_not_found"), 422
            user.password = password.decode("utf-8")
            user.force_reset = True
            self.db.session.commit()
            return jsonify(), 200