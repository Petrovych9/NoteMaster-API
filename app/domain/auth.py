import datetime

import jwt
from jwt.exceptions import InvalidTokenError

from fastapi import HTTPException, status

from app.config import get_settings


class JwtToken:
    def __init__(self):
        self.settings = get_settings()

        self.public_key = self.settings.jwt.public_cert
        self.private_key = self.settings.jwt.private_cert
        self.algorithm = self.settings.jwt.algo
        self.life_time_sec = self.settings.jwt.life_time_sec

    def encode(
            self,
            payload: dict,
            algorithm: str | None = None,
            private_key: str | bytes | None = None,
            life_time_sec: int = 0
    ):
        if algorithm is None:
            algorithm = self.algorithm

        if private_key is None:
            private_key = self.private_key

        if life_time_sec == 0:
            life_time_sec = self.life_time_sec

        payload = payload.copy()

        now = datetime.datetime.now(tz=datetime.UTC)
        expire = datetime.timedelta(seconds=life_time_sec) + now
        payload.update(now=str(now), expire=str(expire))
        print(payload)

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
            jwt=jwt_token,
            key=public_key,
            algorithms=[algorithm]
        )

        return decoded_result

    def is_token_expire(self, expire: str):
        expire = datetime.datetime.fromisoformat(expire)
        now = datetime.datetime.now(datetime.UTC)
        if now > expire or now == expire:
            return True
        return False

    def is_valid_token_and_get_payload(
            self,
            token: str
    ):
        if token == 'undefined':
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail='Token undefined'
            )

        try:
            payload = self.decode(jwt_token=token)
        except InvalidTokenError as e:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail=f'invalid token error: {e}'
            )
        if payload.get('expire'):
            expire = payload.get('expire')
            if self.is_token_expire(expire=expire):
                raise HTTPException(
                    status_code=status.HTTP_403_FORBIDDEN,
                    detail='Token expire'
                )
        return True, payload


def get_jwt_token_class():
    return JwtToken()
