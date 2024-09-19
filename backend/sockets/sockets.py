import json
from functools import wraps

from flask import request
from flask_jwt_extended import verify_jwt_in_request, current_user, jwt_required
from flask_jwt_extended.exceptions import NoAuthorizationError, RevokedTokenError, JWTDecodeError
from flask_socketio import namespace, join_room, emit, leave_room, rooms
from jwt import ExpiredSignatureError

from backend.db.models.User import HouseholdMembers, User

from backend.flask_config import app

from .SidManager import general_socket_sid_mapping


def socket_token():
    def wrapper(fn):
        @wraps(fn)
        def decorator(*args, **kwargs):
            try:
                verify_jwt_in_request()
                return fn(*args, **kwargs)
            except NoAuthorizationError as e:
                return "no_authorization", 401
            except ExpiredSignatureError as e:
                return {
                    "code": 401,
                    "status": "expired_signature"
                }
            except RevokedTokenError as e:
                return {
                    "code": 401,
                    "status": "token_revoked"
                }
            except JWTDecodeError as e:
                return {
                    "code": 401,
                    "status": "cannot_decode_token"
                }
            except Exception as e:
                print(e)
                return "error", 500

        return decorator
    return wrapper


def authorize_room(joined=True):
    def wrapper(fn):
        @wraps(fn)
        def decorator(*args, **kwargs):
            room = None
            try:
                room = args[1].get("household", None)
            except:
                pass
            if room is None:
                return 400
            h = HouseholdMembers.query.filter_by(household_id=room, member_id=current_user.id).first()
            if h is None:
                return {
                    "code": 403,
                    "status": "no_member"
                }
            if joined and room not in rooms():
                return {
                    "code": 403,
                    "status": "join_first"
                }
            return fn(*args, **kwargs)
        return decorator
    return wrapper




class HouseholdSocket(namespace.Namespace):

    @socket_token()
    @authorize_room(joined=False)
    def on_join(self, data):
        room = data.pop("household", None)
        if room is None:
            return 403, json.dumps({"status": "error"})
        join_room(room)
        return True, json.dumps({"status": "success"})

    @socket_token()
    @authorize_room()
    def on_leave(self, data):
        username = current_user.username
        room = data.pop("household", None)
        if room is None:
            return 403, json.dumps({"status": "error"})
        leave_room(room)
        emit(room, username + ' has left the room.', to=room, include_self=False)

    @socket_token()
    @authorize_room()
    def on_hi(self, data):
        username = current_user.username
        room = data.pop("household", None)
        if room is None:
            return 400, json.dumps({"status": "error"})
        emit("hi", f"{username} says hi", to=room, include_self=False)
        return "ok"


class GeneralSocket(namespace.Namespace):

    @socket_token()
    def on_connect(self, data):
        general_socket_sid_mapping.add(current_user.username, request.sid)

    @socket_token()
    def on_disconnect(self):
        general_socket_sid_mapping.remove(current_user.username)


    @socket_token()
    def on_username(self, data):
        result = User.query.filter_by(username=data["username"]).first()
        if result is None:
            return {"status": "username_free"}
        return {"status": "username_taken"}

    @socket_token()
    def on_email(self, data):
        result = User.query.filter_by(email=data["email"]).first()
        if result is None:
            return {"status": "email_free"}
        return {"status": "email_taken"}
