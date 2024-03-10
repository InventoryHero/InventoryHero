import uuid
from datetime import datetime, timezone

import sqlalchemy.exc
from flask import Blueprint, request, jsonify
from flask_jwt_extended import create_access_token, jwt_required, current_user, create_refresh_token, get_jwt, \
    decode_token

from backend.mail.Mail import Mail
from backend.db.models.TokenBlacklist import TokenBlacklist
from backend.db.models.User import User as ApplicationUser
import bcrypt

from backend.flask_config import jwt


@jwt.user_identity_loader
def user_identity_lookup(user):
    return user.id


@jwt.user_lookup_loader
def user_lookup_callback(_jwt_header, jwt_data):
    identity = jwt_data["sub"]
    return ApplicationUser.query.filter_by(id=identity).one_or_none()


@jwt.token_in_blocklist_loader
def check_if_token_revoked(jwt_header, jwt_payload: dict) -> bool:
    jti = jwt_payload["jti"]

    token = TokenBlacklist.query.filter_by(jti=jti).scalar()

    return token is not None


class User(Blueprint):
    def __init__(self, name, import_name, application, db, url_prefix, *args):
        self.app = application
        self.db = db

        url_prefix += ("" if url_prefix.endswith("/") else "/") + "user"

        super(User, self).__init__(name=name, import_name=import_name, url_prefix=url_prefix, *args)

        @self.route('/register', methods=["POST"])
        def create_user():
            username = request.json.get("username", None)
            if username is None:
                self.app.logger.error("No or invalid username provided")
                return {"status": "no_username"}, 400

            password = request.json.get("password", None)
            if password is None:
                self.app.logger.error("No password provided")
                return {"status": "no_password"}, 400
            salt = bcrypt.gensalt()

            email = request.json.get("email", None)
            if email is None:
                self.app.logger.error("No or invalid email provided")
                return {"status": "no_email"}, 400

            password = password.encode('utf-8')
            password = bcrypt.hashpw(password, salt)

            self.app.logger.info({
                "username": username,
                "password": password,
                "email": email
            })

            if ApplicationUser.query.filter_by(username=username).count() >= 1:
                return jsonify(status="username_in_use"), 409
            if ApplicationUser.query.filter_by(email=email).count() >= 1:
                return jsonify(status="email_in_use"), 409

            confirmation_code = None
            if self.app.config["CONFIRMATION_NEEDED"]:
                confirmation_code = uuid.uuid4()

            user = ApplicationUser(
                username=username,
                email=email,
                password=password.decode("utf-8"),
                email_confirmed=not self.app.config["CONFIRMATION_NEEDED"],
                confirmation_code=confirmation_code
            )
            self.app.logger.info(confirmation_code)
            if self.app.config["CONFIRMATION_NEEDED"]:
                mail = Mail(self.app.config["SMTP"], self.app.config["APP_URL"])
                mail.send_registration_confirmation(email, confirmation_code)

            try:
                self.db.session.add(user)
                self.db.session.commit()
            except sqlalchemy.exc.IntegrityError as e:
                self.app.logger.error(e)

            return jsonify(
                status="success",
                user=username,
                confirmation=not self.app.config["CONFIRMATION_NEEDED"]
            ), 200


        @self.route("/login", methods=["POST"])
        def login():
            username = request.json.get("username", None)
            if username is None:
                self.app.logger.error("No or invalid username provided")
                return {"status": "no_username"}, 400

            password = request.json.get("password", None)
            if password is None:
                self.app.logger.error("No password provided")
                return {"status": "no_password"}, 400

            user = ApplicationUser.query.filter_by(username=username).first()
            if user is None:
                self.app.logger.error("User does not exist")
                return {"status": "username_not_found"}, 401

            if not user.email_confirmed:
                return jsonify(status="email_not_confirmed"), 403

            pw_valid = bcrypt.checkpw(password.encode('utf-8'), user.password.encode('utf-8'))
            if not pw_valid:
                return {"status": "username_or_pw_invalid"}, 401

            access_token = create_access_token(identity=user)
            refresh_token = create_refresh_token(identity=user)
            return jsonify(access_token=access_token, refresh_token=refresh_token)

        @self.route("", methods=["GET"])
        @jwt_required()
        def get_user():
            #household = HouseholdMembers.query.filter_by(member_id=current_user.id).first()
            return {
                "id": current_user.id,
                "username": current_user.username,
                "email": current_user.email,
                #"household": household.household.to_dict() if household is not None else None
            }, 200

        @self.route("/refresh_token", methods=["POST"])
        @jwt_required(refresh=True)
        def refresh():
            access_token = create_access_token(identity=current_user)
            return jsonify(access_token=access_token)



        @self.route("/logout", methods=["DELETE"])
        @jwt_required()
        def logout():
            refresh_token = request.json["refreshToken"]
            refresh_token = decode_token(refresh_token)
            self.app.logger.info(refresh_token)
            self.blacklist_token(refresh_token)
            self.blacklist_token(get_jwt())

            return jsonify(status="Refresh & access token successfully revoked"), 200

        @self.route("/user_info", methods=["GET"])
        @jwt_required()
        def userpage():
            return jsonify(current_user), 200

        @self.route("/confirm/<string:code>", methods=["POST"])
        def confirm(code):
            code = uuid.UUID(code)
            user = ApplicationUser.query.filter_by(confirmation_code=code).first()
            if user is None:
                return jsonify(status="invalid_code"), 208

            user.confirmation_code = None
            user.email_confirmed = True
            self.db.session.commit()
            return jsonify(), 200




    def blacklist_token(self, token):
        jti = token["jti"]
        ttype = token["type"]
        now = datetime.now(timezone.utc)
        blacklisted = TokenBlacklist(jti=jti, type=ttype, created_at=now)
        self.db.session.add(blacklisted)
        self.db.session.commit()

