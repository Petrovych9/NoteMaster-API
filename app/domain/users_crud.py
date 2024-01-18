from app.domain.abc import UsersDatabaseCrud
from app.domain.users_models import UserModelCreate
from app.utilts import get_pass_hash


class UsersCrud:
    def __init__(self, user_db: UsersDatabaseCrud):
        self.user_db = user_db

    def get_by_email(self, user_email: str):
        field_value = dict(email=user_email)
        user = self.user_db.get(field_value)
        return user

    def get_by_id(self, user_id: int):
        field_value = dict(id=user_id)
        user = self.user_db.get(field_value)
        return user

    def create(self, email: str, password: str, nickname: str = 'nick'):
        user = UserModelCreate(
            email=email,
            password=get_pass_hash(password),
            nickname=nickname
        ).model_dump()
        user_id = self.user_db.create(user)
        return user_id

    def update(self, user_id: int, field_value: dict):
        filter_by = dict(id=user_id)
        updated_user_id = self.user_db.update(
            filter_by=filter_by,
            field_value=field_value
        )
        return updated_user_id

    def delete(self, user_id: int):
        try:
            self.user_db.delete(user_id)
            return f'User with id: {user_id} has been deleted'
        except Exception:
            raise 'Del user error'


def get_users_crud():
    return UsersCrud(UsersDatabaseCrud())


def get_test_users_crud():
    return UsersCrud(UsersDatabaseCrud(tests=True))
