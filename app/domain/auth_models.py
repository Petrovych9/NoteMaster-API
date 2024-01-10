from pydantic import BaseModel


class AuthTokenModelCreate(BaseModel):
    token: str
    user_id: int


class TokenInfo(BaseModel):
    access_token: str
    token_type: str
