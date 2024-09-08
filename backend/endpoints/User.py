import uuid
from datetime import datetime, timezone, timedelta

import sqlalchemy.exc
from flask import Blueprint, request, jsonify
from flask_jwt_extended import create_access_token, jwt_required, current_user, create_refresh_token, get_jwt, \
    decode_token, set_access_cookies

from backend.mail.Mail import Mail
from backend.db.models.TokenBlacklist import TokenBlacklist
from backend.db.models.User import User as ApplicationUser, HouseholdMembers, Household
from backend.db.models.PasswordResetRequests import PasswordResetRequests as PasswordResetRequest
import bcrypt

from backend.flask_config import jwt
from backend.decorators import admin_required

from hashlib import sha256


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
        def register():
            username = request.json.get("username", None)
            if username is None:
                self.app.logger.error("No or invalid username provided")
                return {"status": "no_username"}, 400

            password = request.json.get("password", None)
            if password is None:
                self.app.logger.error("No password provided")
                return {"status": "no_password"}, 400

            email = request.json.get("email", None)
            if email is None:
                self.app.logger.error("No or invalid email provided")
                return {"status": "no_email"}, 400

            salt = bcrypt.gensalt()
            password = password.encode('utf-8')
            password = bcrypt.hashpw(password, salt)

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
            return {
                "id": current_user.id,
                "username": current_user.username,
                "email": current_user.email,
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

        @self.route("/update/<int:user_id>", methods=["POST"])
        @self.route("/update", defaults={'user_id': None}, methods=["POST"])
        @jwt_required()
        @admin_required()
        def update_user(user_id):
            if user_id is None:
                user_id = current_user.id
            to_update = ApplicationUser.query.filter_by(id=user_id).first()
            if to_update is None:
                return jsonify(status="user_not_found"), 400

            username = request.json.get("username", None)
            firstname = request.json.get("first_name", None)
            lastname = request.json.get("last_name", None)
            email = request.json.get("email", None)
            is_admin = request.json.get("is_admin", None)

            existing = ApplicationUser.query.filter((ApplicationUser.username == username) | (ApplicationUser.email == email)).first()

            if existing is not None:
                return jsonify(status="username_or_email_already_exists"), 400
            self.app.logger.info(firstname)
            if username is not None:
                to_update.username = username
            if firstname is not None:
                to_update.first_name = firstname
            if lastname is not None:
                to_update.last_name = lastname
            if email is not None:
                to_update.email = email


            # TODO REFACTOR
            admins = len(ApplicationUser.query.filter_by(is_admin=True).all()) > 1
            status = "updated_successfully"
            if is_admin is not None:
                # check if there is at least one admin left
                if is_admin:
                    to_update.is_admin = is_admin
                elif admins:
                    to_update.is_admin = is_admin
                else:
                    status = "update_successful_admin_remains"
            self.db.session.commit()
            return jsonify(status=status, user=to_update), 200

        @self.route("/create", methods=["POST"])
        @jwt_required()
        @admin_required()
        def create_user():
            username = request.json.get("username", None)
            password = request.json.get("password", None)
            email = request.json.get("email", None)
            lastname = request.json.get("lastname", None)
            firstname = request.json.get("firstname", None)
            is_admin = request.json.get("is_admin", False)
            if username is None:
                return jsonify(status="no_username"), 422
            if password is None:
                return jsonify(status="no_password"), 422
            if email is None:
                return jsonify(status="no_email"), 422

            salt = bcrypt.gensalt()
            password = password.encode('utf-8')
            password = bcrypt.hashpw(password, salt)

            confirmation_code = None
            email_confirmed = True
            if self.app.config["CONFIRMATION_NEEDED"]:
                confirmation_code = uuid.uuid4()
                email_confirmed = False

            user = ApplicationUser.query.filter_by(username=username).first()
            if user is not None:
                return jsonify(status="username_taken"), 422
            user = ApplicationUser.query.filter_by(email=email).first()
            if user is not None:
                return jsonify(status="email_taken"), 422

            user = ApplicationUser(username=username,
                                   password=password.decode("utf-8"),
                                   last_name=lastname,
                                   first_name=firstname,
                                   is_admin=is_admin,
                                   email_confirmed=email_confirmed,
                                   email=email,
                                   registration_date=datetime.utcnow(),
                                   confirmation_code=confirmation_code)

            self.db.session.add(user)
            self.db.session.commit()

            return jsonify(status="success", user=user), 200

        @self.route("/delete/<int:user_id>", methods=["DELETE"])
        @jwt_required()
        @admin_required()
        def delete_user(user_id):
            # TODO DELETE USER AND HOUSEHOLDS AND SO ON ...
            # IF HOUSEHOLD HAS MEMBER, MAKE ANY MEMBER OWNER
            # IF ONLY ONE ADMIN LEFT: DON'T DELETE
            # TODO ONLY REQUIRE ADMIN IF IT IS NOT OWN USER

            user = ApplicationUser.query.filter_by(id=user_id).first()

            if user is None:
                return jsonify(status="user_not_found"), 422

            admins = len(ApplicationUser.query.filter_by(is_admin=True).all()) > 1
            if user.is_admin and not admins:
                return jsonify(status="delete_not_possible_last_admin"), 422

            households = HouseholdMembers.query.filter_by(member_id=user_id).all()
            for household in households:
                db.session.delete(household)
            households = Household.query.filter_by(creator=user_id).all()

            for household in households:
                other_members = HouseholdMembers.query.filter_by(household_id=household.id).all()
                if len(other_members) != 0:
                    household.creator = other_members[0].member_id
                    continue
                self.db.session.delete(household)

            self.db.session.delete(user)
            self.db.session.commit()
            return jsonify(status="success"), 200

        @self.route("/permissions", methods=["GET"])
        @jwt_required()
        def permissions():
            return jsonify(
                admin=current_user.is_admin
            ), 200

        @self.route("/reset-password/<int:user_id>", defaults={'email': None}, methods=["GET"])
        @self.route("/reset-password/<string:email>", defaults={'user_id': None}, methods=["GET"])
        def reset_password_request(user_id, email):
            #TODO THIS THEN NEEDS EMAIL SENDING
            #TODO MAYBE MAKE A EMAIL CONFIG SECTION AS WELL
            #TODO THIS COULD ALSO BE USED TO VERIFY CONFIGURATION/UPDATE IT IF NEEDED

            if not self.app.config["SMTP"]["in_use"]:
                return jsonify(status="email_not_configured"), 503

            user = None
            if user_id is not None:
                user = ApplicationUser.query.filter_by(id=user_id).first()
            elif email is not None:
                user = ApplicationUser.query.filter_by(email=email).first()

            if user is None:
                return jsonify(), 400

            reset_id = uuid.uuid4().hex
            # TODO ABORT IF NO EMAIL CONFIGURED AND NOTIFY USER
            mail = Mail(self.app.config["SMTP"], self.app.config["APP_URL"])
            to = {
                "email": user.email,
                "username": user.username,
                "first_name": user.first_name
            }
            mail.send_reset_password(to, reset_id)
            reset_hash = sha256(reset_id.encode('utf-8')).hexdigest()
            reset_request = PasswordResetRequest(
                user_id=user.id,
                password_reset_hash=reset_hash,
                password_reset_time=datetime.utcnow()
            )
            self.db.session.add(reset_request)
            self.db.session.commit()
            self.app.logger.info(reset_id)

            return jsonify(status="success_24h_time"), 200

        @self.route("/reset-password/<string:code>", methods=["POST"])
        def reset_password_preflight(code):
            self.app.logger.info(code)
            reset_hash = sha256(code.encode('utf-8')).hexdigest()
            reset_request = PasswordResetRequest.query.filter_by(password_reset_hash=reset_hash).first()
            if reset_request is None:
                return {}, 400
            if reset_request.password_reset_time + timedelta(hours=24) < datetime.utcnow():
                return jsonify(status="expired"), 400
            return {}, 200



    def blacklist_token(self, token):
        jti = token["jti"]
        ttype = token["type"]
        now = datetime.now(timezone.utc)
        blacklisted = TokenBlacklist(jti=jti, type=ttype)
        self.db.session.add(blacklisted)
        self.db.session.commit()

