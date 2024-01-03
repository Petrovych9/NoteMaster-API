from fastapi import Depends, HTTPException, status

from app.domain.token_crud import AuthTokenCrud, get_token_crud
from app.models import AuthToken
from app.domain.error_models import ErrorResponse


def check_auth_token(
        token: str,
        db: AuthTokenCrud = Depends(get_token_crud)
):
    auth_token = db.get_by_field(token=token)
    if not auth_token:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=ErrorResponse.INVALID_TOKEN
        )

    return auth_token
