from flask_jwt_extended import get_current_user

from backend.database import db


class TokenBlacklist(db.Model):
    id: int = db.Column(db.Integer, primary_key=True, autoincrement=True)
    jti: str = db.Column(db.String(36), nullable=False, index=True)
    type: str = db.Column(db.String(16), nullable=False)
    user_id = db.Column(
        db.ForeignKey('user.id', ondelete="CASCADE"),
        default=lambda: get_current_user().id,
        nullable=False,
    )
