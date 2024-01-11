import datetime

import jwt
from jwt.exceptions import InvalidTokenError

from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer

from app.config import get_settings


class JwtToken:
    def __init__(self):
        self.settings = get_settings()

        self.public_key = self.settings.jwt.public_cert
        self.private_key = self.settings.jwt.private_cert
        self.algorithm = self.settings.jwt.algo
        self.life_time = self.settings.jwt.life_time

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

        now = datetime.datetime.utcnow()
        expire = self.life_time + now
        payload.update(now=now, expire=expire)

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

    # def grand_jwt_token_via_login_url(self):
    #     api_version = self.settings.urls.api_version_prefix
    #     prefix = self.settings.urls.users_prefix
    #     endpoint = self.settings.urls.users_endpoints.login
    #     login_url = api_version + prefix + endpoint
    #     print(login_url)
    #     return OAuth2PasswordBearer(login_url)

    def is_valid_token_and_get_payload(
            self,
            token: str
    ):
        try:
            payload = jwt.decode(jwt_token=token)
        except InvalidTokenError as e:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail=f'invalid token error: {e}'
            )

        return True, payload
