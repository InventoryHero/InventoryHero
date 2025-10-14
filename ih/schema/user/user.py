from pydantic import BaseModel, ConfigDict
from typing import Optional
from datetime import datetime
from uuid import UUID


class UserBase(BaseModel):
    username: str
    email: str
    first_name: Optional[str] = None
    last_name: Optional[str] = None

class UserCreateBase(UserBase):
    password: str

class UserCreate(UserCreateBase):
    password_confirmation: str

class AdminUserCreate(UserCreateBase):
    admin: bool = False

class UserUpdate(BaseModel):
    username: Optional[str] = None
    email: Optional[str] = None
    first_name: Optional[str] = None
    last_name: Optional[str] = None

class AdminUserUpdate(UserUpdate):
    admin: Optional[bool] = None


class UserPublic(UserBase):
    id: UUID
    admin: bool
    registered_on: datetime
    confirmed: bool

    model_config = ConfigDict(from_attributes=True)

class ChangePasswordFormBase(BaseModel):
    new_password: str
    new_password_confirmation: str

class ChangePasswordForm(ChangePasswordFormBase):
    current_password: str
    new_password: str
    new_password_confirmation: str


class ResetPasswordForm(BaseModel):
    email: str

class TokenValidationResponse(BaseModel):
    valid: bool
    reason: Optional[str]

class ResetPasswordResponse(TokenValidationResponse):
    pass