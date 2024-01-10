import jwt

from fastapi import Depends, HTTPException, status

from app.domain.token_crud import AuthTokenCrud, get_token_crud
from app.domain.error_models import ErrorResponse
from app.config import get_settings


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


class JwtToken:
    def __init__(self):
        self.settings = get_settings()

        self.public_key = self.settings.jwt.public_cert
        self.private_key = self.settings.jwt.private_cert
        self.algorithm = self.settings.jwt.algo

    def encode(
            self,
            payload: dict,
            algorithm: str | None = None,
            private_key: str | bytes | None = None,
    ):
        if algorithm is None:
            algorithm = self.algorithm

        if private_key is None:
            private_key = self.private_key

        encoded_result = jwt.encode(
            payload=payload,
            key=private_key,
            algorithm=algorithm
        )

        return encoded_result

    def decode(
            self,
            jwt_token: str,
            algorithm: str | None = None,
            public_key: str | bytes | None = None,
    ):

        if algorithm is None:
            algorithm = self.algorithm

        if public_key is None:
            public_key = self.public_key

        decoded_result = jwt.decode(
            jwt_token=jwt_token,
            key=public_key,
            algorithms=[algorithm]
        )

        return decoded_result
