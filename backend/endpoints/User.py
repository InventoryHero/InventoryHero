import uuid
from datetime import datetime, timezone, timedelta, UTC

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

from backend.utils.validation import validate_username, validate_email
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
                return {"status": "no_username"}, 400
            result = validate_username(username)
            if result is not True:
                return jsonify(status="username_invalid"), 400

            password = request.json.get("password", None)
            if password is None:
                return {"status": "no_password"}, 400

            email = request.json.get("email", None)
            if email is None:
                return {"status": "no_email"}, 400
            if not validate_email(email):
                return jsonify(status="email_invalid"), 400

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
                return {"status": "no_username"}, 400

            password = request.json.get("password", None)
            if password is None:
                return {"status": "no_password"}, 400

            user = ApplicationUser.query.filter_by(username=username).first()
            if user is None:
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
            return jsonify(current_user), 200

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
        @jwt_required()
        @admin_required()
        def update_user_admin(user_id):
            to_update = ApplicationUser.query.filter_by(id=user_id).first()
            return update_user(to_update)

        @self.route("/update", methods=["POST"])
        @jwt_required()
        def update_own():
            return update_user(current_user)

        def update_user(to_update):
            if to_update is None:
                return jsonify(status="user_not_found"), 400

            username = request.json.get("username", None)

            firstname = request.json.get("firstName", None)
            lastname = request.json.get("lastName", None)
            email = request.json.get("email", None)
            is_admin = request.json.get("isAdmin", None)
            existing = ApplicationUser.query.filter((ApplicationUser.username == username) | (ApplicationUser.email == email)).first()

            if existing is not None:
                return jsonify(status="username_or_email_already_exists"), 400
            self.app.logger.info(firstname)
            if username is not None:
                result = validate_username(username)
                if result is not True:
                    return jsonify(status="username_invalid"), 400
                to_update.username = username
            if firstname is not None:
                to_update.first_name = firstname
            if lastname is not None:
                to_update.last_name = lastname
            if email is not None:
                if not validate_email(email):
                    return jsonify(status="email_invalid"), 400
                to_update.email = email
                # TODO RESEND EMAIL NOTIFICATION HERE


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
            lastname = request.json.get("lastName", None)
            firstname = request.json.get("firstName", None)
            is_admin = request.json.get("isAdmin", False)
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

            #households = HouseholdMembers.query.filter_by(member_id=user_id).all()
            #for household in households:
            #    db.session.delete(household)
            #households = Household.query.filter_by(creator=user_id).all()#

            #for household in households:
            #    other_members = HouseholdMembers.query.filter_by(household_id=household.id).all()
            #    if len(other_members) != 0:
            #        household.creator = other_members[0].member_id
            #        continue
            #    self.db.session.delete(household)

            self.db.session.delete(user)
            self.db.session.commit()
            return jsonify(status="success"), 200

        @self.route("/permissions", methods=["GET"])
        @jwt_required()
        def permissions():
            return jsonify(
                admin=current_user.is_admin
            ), 200

        @self.route("/reset-password/<int:user_id>", methods=["GET"])
        @jwt_required()
        @admin_required()
        def reset_password_request_admin(user_id):
            user = ApplicationUser.query.filter_by(id=user_id).first()
            if user is None:
                return jsonify(), 400
            return request_password_reset_mail(user)

        @self.route("/reset-password/<string:email>", methods=["GET"])
        def reset_password_request_email(email):
            user = ApplicationUser.query.filter_by(email=email).first()
            return request_password_reset_mail(user)

        @self.route("/reset-password", methods=["GET"])
        @jwt_required()
        def reset_password_request_current_user():
            return request_password_reset_mail(current_user)

        def request_password_reset_mail(user):
            if not self.app.config["SMTP"]["in_use"]:
                return jsonify(status="email_not_configured"), 503
            if user is None:
                return jsonify(), 200
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

        @self.route("/reset-password", methods=["POST"])
        @jwt_required()
        def reset_password_with_old_password():
            old_password = request.json.get("oldPassword", None)
            new_password = request.json.get("newPassword", None)
            if old_password is None or new_password is None:
                return jsonify(status="no_password"), 400
            pw_valid = bcrypt.checkpw(old_password.encode('utf-8'), current_user.password.encode('utf-8'))
            if not pw_valid:
                return jsonify(status="password_invalid"), 403
            salt = bcrypt.gensalt()
            new_password = new_password.encode('utf-8')
            new_password = bcrypt.hashpw(new_password, salt)
            current_user.password = new_password.decode("utf-8")
            current_user.force_reset = False
            self.db.session.commit()
            return jsonify(), 200

        @self.route("/reset-password/<string:token>", methods=["POST"])
        def reset_password_with_token(token):
            password = request.json.get("password", None)
            if password is None:
                return jsonify(status="no_password"), 400
            is_valid, msg, password_request = is_reset_token_valid(token)
            if not is_valid:
                return jsonify(status=msg), 403
            user = ApplicationUser.query.filter_by(id=password_request.user_id).first()
            if user is None:
                return jsonify(status="user_not_found"), 400

            salt = bcrypt.gensalt()
            password = bcrypt.hashpw(password.encode('utf-8'), salt)
            user.password = password.decode("utf-8")
            user.force_reset = False
            self.db.session.delete(password_request)
            self.db.session.commit()
            return jsonify(), 200

        @self.route("/reset-password/<string:code>", methods=["PUT"])
        def reset_password_preflight(code):
            self.app.logger.error("OPTIONS")
            is_valid, msg, _ = is_reset_token_valid(code)
            if not is_valid:
                return jsonify(status=msg), 400
            return jsonify(), 200

        def is_reset_token_valid(code):
            reset_hash = sha256(code.encode('utf-8')).hexdigest()
            reset_request = PasswordResetRequest.query.filter_by(password_reset_hash=reset_hash).first()
            self.app.logger.info(reset_request)
            if reset_request is None:
                return False, "invalid_token", None
            if reset_request.password_reset_time + timedelta(hours=24) < datetime.now(UTC):
                return False, "expired", None
            return True, "", reset_request

    def blacklist_token(self, token):
        jti = token["jti"]
        ttype = token["type"]
        now = datetime.now(timezone.utc)
        blacklisted = TokenBlacklist(jti=jti, type=ttype)
        self.db.session.add(blacklisted)
        self.db.session.commit()

