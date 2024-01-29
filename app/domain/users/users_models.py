from typing import Optional

from pydantic import BaseModel

from app.domain.base_models import BaseModelResponse, GetBase


class CreateUserRequest(BaseModel):
    email: str
    password: str
    nickname: Optional[str] = None


class CreateUserResponse(BaseModelResponse):
    user_id: int


class UserModel(CreateUserRequest):
    id: int
    created_at: str


class RefreshAccessTokenRequest(BaseModel):
    refresh_token: str
    update_refresh_token: bool = False,


class RefreshAccessTokenResponse(BaseModel):
    access_token: str
    refresh_token: str


class GetUserResponse(BaseModelResponse):
    user_id: int
    email: str
    nickname: str
