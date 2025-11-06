from datetime import datetime
from typing import Annotated
from uuid import UUID
from authlib.integrations.starlette_client import OAuth
from fastapi import APIRouter, Depends, HTTPException, Form, Response, Request
from pydantic import BaseModel
from sqlmodel import Session, select
from starlette import status
from starlette.datastructures import URLPath
from starlette.responses import RedirectResponse
from ih.i18n import get_localizer
from ih.core.config import get_app_settings
from ih.core.exceptions.exceptions import InventoryHeroAPIException
from ih.core.logging.logger import get_logger
from ih.core.security.password import verify_password, create_access_token, create_refresh_token
from ih.core.security import settings, ALGORITHM
from ih.db.db_setup import get_session
from ih.db.models.RefreshToken import RefreshToken
from ih.db.models.User import User, AuthenticationProvider
from ih.i18n.localizer import Localizer
from ih.repositories.factory import RepositoryFactory
from ih.routes._base.UserApiRouter import UserAPIRouter

import jwt

from ih.schema.common.error_response import ErrorResponse
from ih.schema.user import UserBase
from ih.schema.user.user import ResetPasswordForm, UserCreate, UserCreateBase

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

logger = get_logger()
settings = get_app_settings()



if settings.OIDC.enabled:
    oauth = OAuth()
    oidc = oauth.register(
        name="oidc", # TODO MAYBE NAME PROVIDER
        client_id = settings.OIDC.IH_OIDC_CLIENT_ID,
        client_secret = settings.OIDC.IH_OIDC_CLIENT_SECRET,
        server_metadata_url=settings.OIDC.IH_OIDC_CONFIGURATION_URL,
        client_kwargs={"scope": "openid profile email"} # TODO CONFIGURE
    )

def generate_tokens(user_id: UUID,  response: Response, session: Session, ) -> None:
    token_payload = {
            "sub": str(user_id)
        }
    access_token = create_access_token(token_payload)
    refresh_token, jti = create_refresh_token(token_payload, session, user_id)

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


@public_router.post("/token")
async def get_token(
        response: Response,
        form_data: Annotated[CredentialsRequestForm, Depends()],
        session: Session = Depends(get_session)
) -> None:
    query = select(User).filter_by(username=form_data.username)

    user = session.exec(query).first()

    if user is None:
        raise InventoryHeroAPIException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=ErrorResponse(
                message="username_or_password_incorrect",
                toast=False
            )
        )


    if not verify_password(form_data.password, user.password):
        raise InventoryHeroAPIException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=ErrorResponse(
                message="username_or_password_incorrect",
                toast=False
            ),
            headers={"WWW-Authenticate": "Bearer"},
        )

    generate_tokens(user.id, response, session)


@public_router.get("/oidc/token")
async def get_oidc_token(request: Request):
    if not oauth:
        raise InventoryHeroAPIException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail=ErrorResponse(
                message="", # TODO
                toast = False
            )
        )
    client = oauth.create_client("oidc")
    if not settings.PRODUCTION:
        redirect_url = "https://localhost:3000/login"
    else:
        redirect_url = URLPath("/login").make_absolute_url(request.base_url)

    redirect_url = "http://localhost:5000/api/auth/oidc/callback"
    return await client.authorize_redirect(request, redirect_url)

@public_router.get("/oidc/callback")
async def oidc_callback(request: Request, session: Session = Depends(get_session), localizer:Localizer =  Depends(get_localizer)):
    client = oauth.create_client("oidc")
    token = await client.authorize_access_token(request)
    user_info = token["userinfo"]
    repositories = RepositoryFactory(session, localizer)
    oidc_sub = user_info["sub"]
    user = repositories.users.get_user_by_oidc_sub(oidc_sub)

    if not settings.PRODUCTION:
        redirect_url = "https://localhost:3000/login"
    else:
        redirect_url = URLPath("/login").make_absolute_url(request.base_url)


    if user:
        logger.info(f"OIDC user with SUB {oidc_sub} found")
    if settings.OIDC.user_claim == "preferred_username":
       user = repositories.users.get_user_by_username(user_info[settings.OIDC.user_claim])
    elif settings.OIDC.user_claim == "email":
        user = repositories.users.get_user_by_email(user_info[settings.OIDC.user_claim])
    else:
        # TODO IF VALIDATION IS GOOD ENOUGH THIS SHOULD NOT HAPPEN
        pass

    try:
        if user is None:
            logger.info("OIDC USER DOES NTO EXIST, CREATING WITH OIDC DATA")
            user = repositories.users.create(UserCreateBase(
                username=user_info["preferred_username"],
                email=user_info["email"],
                auth_provider=AuthenticationProvider.oidc,
                password='oidc_user'
            ), False)
        elif user.auth_provider != AuthenticationProvider.oidc:
            repositories.users.update_auth_provider(user, AuthenticationProvider.oidc, oidc_sub)
            logger.info(f"user exists already {user}, migrated to OIDC")


        last_name = user_info["name"]
        first_name = user_info["given_name"]
        email = user_info["email"]
        username = user_info["preferred_username"]
        repositories.users.update_against_auth_provider(user, last_name, first_name, email, username)
    except InventoryHeroAPIException as e:
        if e.status_code == status.HTTP_409_CONFLICT:
            logger.error("User with conflicting info already exists")
            return RedirectResponse(url=redirect_url + "?error=conflict")
    except Exception as e:
        logger.error(e)
        return RedirectResponse(url=redirect_url + "?error=unknown_error")

    response = RedirectResponse(url=redirect_url)
    generate_tokens(user.id, response, session)
    return response

@public_router.get("/refresh")
async def refresh(response: Response, request: Request, session: Session = Depends(get_session)):
    refresh_token = request.cookies.get("refresh_token")
    # TODO MAYBE QUERY OIDC PROVIDER HERE?
    if not refresh_token:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="refresh_token_not_found")

    try:
        payload = jwt.decode(refresh_token, settings.IH_SECRET_KEY, algorithms=[ALGORITHM])
        uuid = payload.get("sub")
        token_row = session.get(RefreshToken, payload.get("jti"))

        if not uuid or not token_row:
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

    new_access_token = create_access_token({"sub": uuid})
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
        logger.error(e)
    finally:
        response.delete_cookie("refresh_token", path="/api/auth")
        response.delete_cookie("access_token", path="/")
        return {"detail": "Logged out"}

