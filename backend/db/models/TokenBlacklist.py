from flask_jwt_extended import get_current_user
from sqlalchemy.sql import func


from backend.database import db
from backend.db.base import Base


class TokenBlacklist(db.Model, Base):
    id: int = db.Column(db.Integer, primary_key=True, autoincrement=True)
    jti: str = db.Column(db.String(36), nullable=False, index=True)
    type: str = db.Column(db.String(16), nullable=False)
    user_id = db.Column(
        db.ForeignKey('user.id'),
        default=lambda: get_current_user().id,
        nullable=False,
    )
    created_at = db.Column(
        db.DateTime,
        server_default=func.now(),
        nullable=False,
    )