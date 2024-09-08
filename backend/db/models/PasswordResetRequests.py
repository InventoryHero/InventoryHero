import datetime
from dataclasses import dataclass
from backend.database import db


@dataclass
class PasswordResetRequests(db.Model):
    id: int = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_id = db.Column(
        db.ForeignKey('user.id'),
        nullable=False,
    )
    password_reset_hash: str = db.Column(db.String(1024), nullable=False)
    password_reset_time: datetime = db.Column(db.DateTime(timezone=True), default=lambda: datetime.datetime.now(datetime.UTC), nullable=False)
