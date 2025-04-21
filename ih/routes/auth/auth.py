from datetime import datetime
from typing import Annotated
from fastapi import APIRouter, Depends, HTTPException, Form, Response, Request
from pydantic import BaseModel
from sqlmodel import Session, select
from starlette import status
from ih.core.security.password import verify_password, create_access_token, create_refresh_token
from ih.core.security import settings, ALGORITHM
from ih.db.db_setup import get_session
from ih.db.models.RefreshToken import RefreshToken
from ih.db.models.User import User
from ih.routes._base.UserApiRouter import UserAPIRouter

import jwt

public_router = APIRouter(tags=["authentication"])
user_router = UserAPIRouter(tags=["authentication"])

class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    username: str | None = None


class CredentialsRequestForm:
    def __init__(
        self,
        username: str = Form(""),
        password: str = Form("")
    ):
        self.username = username
        self.password = password


@public_router.post("/token")
async def get_token(
        response: Response,
        form_data: Annotated[CredentialsRequestForm, Depends()],
        session: Session = Depends(get_session)
) -> Token:
    query = select(User).filter_by(username=form_data.username)

    user = session.exec(query).first()

    if user is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="user_not_found"
        )


    if not verify_password(form_data.password, user.password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="username_or_password_incorrect",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token = create_access_token(
        {
            "sub": user.username
        }
    )
    refresh_token, jti = create_refresh_token({"sub": user.username}, session, user.id)

    response.set_cookie(
        key="refresh_token",
        value=refresh_token,
        httponly=True,
        secure=settings.PRODUCTION,
        samesite="strict",
        max_age=settings.IH_REFRESH_TOKEN_EXPIRATION,
        path="/api/auth"
    )

    response.set_cookie(
        key="access_token",
        value=access_token,
        httponly=True,
        secure=settings.PRODUCTION,
        samesite="strict",
        max_age=settings.IH_ACCESS_TOKEN_EXPIRATION,
        path="/"
    )

    return Token(access_token=access_token, token_type="bearer")


@public_router.get("/refresh")
async def refresh(response: Response, request: Request, session: Session = Depends(get_session)):
    refresh_token = request.cookies.get("refresh_token")
    if not refresh_token:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="refresh_token_not_found")

    try:
        payload = jwt.decode(refresh_token, settings.IH_SECRET_KEY, algorithms=[ALGORITHM])
        username = payload.get("sub")
        token_row = session.get(RefreshToken, payload.get("jti"))

        if not username or not token_row:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="invalid_token",
            )
        if token_row.expires_at <= datetime.now():
            session.delete(token_row)
            session.commit()
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="refresh_token_expired",
            )

    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="invalid_token",
        )

    new_access_token = create_access_token({"sub": username})
    response.set_cookie(
        key="access_token",
        value=new_access_token,
        httponly=True,
        secure=settings.PRODUCTION,
        samesite="strict",
        max_age=settings.IH_ACCESS_TOKEN_EXPIRATION,
        path="/"
    )
    return {"access_token": new_access_token, "token_type": "bearer"}


@user_router.post("/logout")
def logout(response: Response, request: Request, session: Session = Depends(get_session)):
    refresh_token = request.cookies.get("refresh_token")
    try:
        payload = jwt.decode(refresh_token, settings.IH_SECRET_KEY, algorithms=[ALGORITHM])
        query = select(RefreshToken).where(RefreshToken.jti == payload.get("jti"))
        token_row = session.exec(query).first()
        if not token_row:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="invalid_token"
            )
        session.delete(token_row)
        session.commit()
    except Exception as e:
        # TODO log error

        pass
    finally:
        response.delete_cookie("refresh_token", path="/api/auth")
        response.delete_cookie("access_token", path="/")
        return {"detail": "Logged out"}