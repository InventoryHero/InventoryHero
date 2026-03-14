import uuid
from datetime import timedelta, datetime, timezone, UTC
from pwdlib import PasswordHash
from sqlmodel import Session
from uuid import UUID

from . import settings, ALGORITHM

import jwt

from ..logging.logger import get_logger
from ...db.models.RefreshToken import RefreshToken

password_hash = PasswordHash.recommended()
logger = get_logger()

def verify_password(plain_password: str, hashed_password: str) -> bool:
    return password_hash.verify(plain_password, hashed_password)

def hash_password(plain_password: str) -> str:
    return password_hash.hash(plain_password)

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

def token_expires_soon(exp, threshold_seconds: int = 60):
    try:
        exp = datetime.fromtimestamp(exp, UTC)
        return (exp - datetime.now(UTC)).total_seconds() < threshold_seconds
    except Exception as ex:
        logger.error(ex)
        pass
    return False
