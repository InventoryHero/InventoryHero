import uuid
from datetime import timedelta, datetime, timezone
from passlib.context import CryptContext
from sqlmodel import Session
from uuid import UUID

from . import settings, ALGORITHM

import jwt

from ...db.models.RefreshToken import RefreshToken

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)

def hash_password(plain_password: str) -> str:
    return pwd_context.hash(plain_password)

def create_access_token(data: dict):
    to_encode = data.copy()
    expire = datetime.now(timezone.utc) + timedelta(seconds=settings.IH_ACCESS_TOKEN_EXPIRATION)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, settings.IH_SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

def create_refresh_token(data: dict, session: Session, user_id: UUID):
    to_encode = data.copy()
    expire = datetime.now(timezone.utc) + timedelta(seconds=settings.IH_REFRESH_TOKEN_EXPIRATION)
    jti = str(uuid.uuid4())
    to_encode.update({"jti": jti, "exp": expire})
    encoded_jwt = jwt.encode(to_encode, settings.IH_SECRET_KEY, algorithm=ALGORITHM)
    session.add(RefreshToken(jti=jti, user_id=user_id, expires_at=expire, revoked=False))
    session.commit()
    return encoded_jwt, jti