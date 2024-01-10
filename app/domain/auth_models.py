from pydantic import BaseModel


class AuthTokenModelCreate(BaseModel):
    token: str
    user_id: int

