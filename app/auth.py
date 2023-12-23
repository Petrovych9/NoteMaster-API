from fastapi import Depends, HTTPException, status

from app.models import AuthToken
from app.db import get_db_session
from app.models import ErrorResponse


def check_auth_token(
        token: str,
        db=Depends(get_db_session)
):
    auth_token = db.query(AuthToken).filter(AuthToken.token == token).one_or_none()

    if not auth_token:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail=ErrorResponse.INVALID_TOKEN
        )

    return auth_token
