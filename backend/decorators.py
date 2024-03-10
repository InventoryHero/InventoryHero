import uuid
from functools import wraps

from flask import jsonify
from flask_jwt_extended import current_user

from backend.endpoints.Helper import user_in_household
from backend.flask_config import socketio


def auth(f):
    @wraps(f)
    def decorator(*args, **kwargs):
        household_id = kwargs.get('household', None)
        if household_id is None:
            return jsonify(status="no_household_set"), 400

        in_household = user_in_household(current_user.id, household_id)
        if not in_household:
            return jsonify(status="user_not_in_household"), 401
        return f(*args, **kwargs)
    return decorator


def emit_update():
    def wrapper(fn):
        @wraps(fn)
        def decorator(*args, **kwargs):
            response = fn(*args, **kwargs)
            household = kwargs.get('household', None)

            # emit if success
            if 200 <= response[1] <= 299:
                socketio.emit("new-content", {
                    "user": current_user.username
                }, to=household, namespace='/household')

            return response
        return decorator
    return wrapper

