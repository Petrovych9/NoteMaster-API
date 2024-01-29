from pydantic import BaseModel

from app.config import get_settings


class AuthTokenModelCreate(BaseModel):
    token: str
    user_id: int
    expire: str
