from fastapi import Depends, HTTPException
from starlette import status

from app.models import AuthToken, connect_db


def check_auth_token(
        token: str,
        db=Depends(connect_db)
):
    auth_token = db.query(AuthToken).filter(AuthToken.token == token).one_or_none()

    if not auth_token:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail='AUTH_TOKEN_NOT_FOUND'
        )

    return auth_token
