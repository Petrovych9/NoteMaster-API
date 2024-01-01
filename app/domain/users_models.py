from typing import Optional

from pydantic import BaseModel


class UserLoginForm(BaseModel):
    email: str
    password: str


class UserCreateForm(UserLoginForm):
    nickname: Optional[str] = None


class UserModelCreate(UserCreateForm):
    pass


class UserModel(UserModelCreate):
    id: int
    created_at: str


