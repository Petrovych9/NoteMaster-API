from typing import Tuple, Annotated

from fastapi import HTTPException, status, Depends


from app.domain.error_models import ErrorResponse
from app.domain.auth.auth_models import AuthTokenModelCreate
from app.domain.notes_category.note_categories_models import \
    CreateNoteCategoryRequest
from app.domain.users.users_crud import get_users_crud
from app.domain.auth.token_crud import get_token_crud
from app.domain.auth.auth import get_jwt_token_class
from app.domain.notes_category.note_categories_crud import get_notes_categories_crud
from app.config import get_settings
from app.domain.users.users_models import UserModel


class Helper:
    def __init__(self):
        self.settings = get_settings()

        self.user_db = get_users_crud()
        self.token_db = get_token_crud()
        self.note_category_db = get_notes_categories_crud()

        self.jwt = get_jwt_token_class()

    def get_current_user(
            self,
            token: str,
    ) -> UserModel:
        jwt = get_jwt_token_class()
        users_crud = get_users_crud()

        is_valid_token, decoded_payload = jwt.is_valid_token_and_get_payload(
            token)
        if not is_valid_token or not decoded_payload:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail='Error during decoding token'
            )
        user = users_crud.get_by_email(
            user_email=decoded_payload.get('email')
        )
        if not user:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail=ErrorResponse.USER_NOT_FOUND
            )

        return user

    def get_category_id_by_name_or_create_new(self, category_name) -> int:
        category = self.note_category_db.get_by_name(
            category_name=category_name)
        if not category:
            created_new_category_id = self.note_category_db.create(
                CreateNoteCategoryRequest(name=category_name)
            )
            if not created_new_category_id:
                raise HTTPException(
                    status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                    detail=ErrorResponse.CREATING_NOTE_ERROR
                )
            return created_new_category_id
        return category.id


def get_helper():
    return Helper()
