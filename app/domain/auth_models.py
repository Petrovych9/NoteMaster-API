from pydantic import BaseModel

from app.config import get_settings


class AuthTokenModelCreate(BaseModel):
    token: str
    user_id: int
    expire: str


class TokenInfo(BaseModel):
    access_token: str
    refresh_token: str
    token_type: str = get_settings().jwt.type
