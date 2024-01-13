from fastapi import Depends, HTTPException, status

from app.domain.error_models import ErrorResponse
from app.domain.auth_models import AuthTokenModelCreate
from app.domain.users_crud import UsersCrud, get_users_crud
from app.domain.token_crud import AuthTokenCrud, get_token_crud
from app.domain.auth import JwtToken
from app.utilts import get_pass_hash
from app.config import get_settings


class Validator:
    def __init__(
            self,
            user_db: UsersCrud = Depends(get_users_crud),
            token_db: AuthTokenCrud = Depends(get_token_crud),
            jwt: JwtToken = Depends(JwtToken)
    ):
        self.settings = Depends(get_settings)

        self.user_db = user_db
        self.token_db = token_db
        self.jwt = jwt

    def check_user(
            self,
            email: str,
            password: str
    ) -> tuple[bool, int]:
        if not email or not password:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=ErrorResponse.INTERNAL_ERR0R
            )

        user = self.user_db.get_by_email(user_email=email)
        if not user:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail=ErrorResponse.INVALID_EMAIL
            )
        elif password != user.password:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail=ErrorResponse.INVALID_PASSWORD
            )

        return True, user.id

    def check_auth_token(
            self,
            token: str,
    ) -> AuthTokenModelCreate:
        is_valid, payload = self.jwt.is_valid_token_and_get_payload(token)

        auth_token = self.token_db.get_by_field(token=token)
        if not auth_token:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=ErrorResponse.INVALID_TOKEN
            )

        return auth_token