from pydantic import BaseModel, ConfigDict
from typing import Optional
from datetime import datetime


class UserBase(BaseModel):
    username: str
    email: str
    first_name: Optional[str] = None
    last_name: Optional[str] = None

class UserCreate(UserBase):
    password: str

class AdminUserCreate(UserCreate):
    admin: bool = False

class UserPublic(UserBase):
    id: int
    admin: bool
    registered_on: datetime
    confirmed: bool

    model_config = ConfigDict(from_attributes=True)