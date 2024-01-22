# from app.db import get_db_session
from app.domain.abc import AuthTokenDatabaseCrud
from app.domain.auth.auth_models import AuthTokenModelCreate


class AuthTokenCrud:
    def __init__(self, token_db: AuthTokenDatabaseCrud):
        self.token_db = token_db

    def get_by_field(
            self,
            token_id: int = None,
            user_id: int = None,
            token: str = None
    ):
        field_value = dict(user_id=user_id)
        if token_id:
            field_value = dict(id=token_id)
        if token:
            field_value = dict(token=token)

        token = self.token_db.get(field_value)
        return token

    def create(self, token: str, user_id: int, expire: str):
        auth_token = AuthTokenModelCreate(
            token=token,
            user_id=user_id,
            expire=str(expire)
        )
        auth_token_id = self.token_db.create(auth_token.model_dump())
        return auth_token_id

    def update(self, field_value: dict,  token_id: int = None, user_id: int = None):
        filter_by = dict(
            user_id=user_id
        )
        if token_id:
            filter_by = dict(
                id=token_id
            )
        updated_user_id = self.token_db.update(
            filter_by=filter_by,
            field_value=field_value
        )
        return updated_user_id

    def delete(self, token_id: int):
        try:
            self.token_db.delete(token_id)
            return f'AuthToken with id: {token_id} has been deleted'
        except Exception:
            raise 'Del token error'


def get_token_crud():
    return AuthTokenCrud(AuthTokenDatabaseCrud())


def get_test_token_crud():
    return AuthTokenCrud(AuthTokenDatabaseCrud(tests=True))
