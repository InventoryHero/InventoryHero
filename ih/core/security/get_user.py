from fastapi import Depends, HTTPException, Request, status, Path
from fastapi.security import OAuth2PasswordBearer
from jwt import PyJWTError, ExpiredSignatureError
import jwt
from sqlmodel import select, Session
from uuid import UUID

from ih.db.db_setup import get_session
from ih.db.models.User import User
from . import settings, ALGORITHM
from ...db.models.households import HouseholdMember
from ...schema.households import Role

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/auth/token", auto_error=False)


credentials_exception = HTTPException(
    status_code=status.HTTP_401_UNAUTHORIZED,
    detail="invalid_credentials",
    headers={"WWW-Authenticate": "Bearer"},
)



async def try_get_current_user(
    request: Request,
    token: str | None = Depends(oauth2_scheme),
    session=Depends(get_session),
) -> User | None:
    try:
        return await get_current_user(request, token, session)
    except Exception:
        return None


async def get_current_user(
    request: Request,
    token: str | None = Depends(oauth2_scheme),
    session=Depends(get_session),
) -> User:
    if token is None:
        token = request.cookies.get("access_token")
    try:
        payload = jwt.decode(token, settings.IH_SECRET_KEY, algorithms=[ALGORITHM])
        uuid_str: str | None = payload.get("sub")
        if uuid_str is None:
            raise credentials_exception
        uuid: UUID = UUID(uuid_str)
    except PyJWTError:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED)

    query = select(User).where(User.id == uuid)
    user = session.exec(query).first()

    if user is None:
        raise credentials_exception
    return user

async def get_admin_user(current_user: User = Depends(get_current_user)) -> User:
    if not current_user.admin:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN)
    return current_user


async def get_household_member(
    household_id: UUID = Path(...),
    db: Session = Depends(get_session),
    user: User = Depends(get_current_user)
) -> Role | None:
    membership = db.exec(
        select(HouseholdMember).where(
            (HouseholdMember.household_id == household_id),
            (HouseholdMember.user_id == user.id)
        )
    ).first()

    if not membership:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="no_member_of_household")

    return membership.role

async def get_household_id(
    household_id: UUID = Path(...)
) -> UUID | None:
    return household_id

def get_household_admin_or_owner(
    household_id: UUID = Path(...),
    db: Session = Depends(get_session),
    user: User = Depends(get_current_user)
) -> Role | None:
    membership = db.exec(
        select(HouseholdMember).where(
            (HouseholdMember.household_id == household_id),
            (HouseholdMember.user_id == user.id)
        )
    ).first()

    if not membership or membership.role not in [Role.ADMIN, Role.OWNER]:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="invalid_permissions_to_manage_household"
        )
    return membership.role