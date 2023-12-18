from pydantic import BaseModel
from typing import Optional


class UserLoginForm(BaseModel):
    email: str
    password: str


class UserCreateForm(UserLoginForm):
    nickname: Optional[str] = None
