from fastapi import Depends, HTTPException, status

from app.domain.error_models import ErrorResponse
from app.domain.users_crud import UsersCrud, get_users_crud
from app.utilts import get_pass_hash
from app.config import get_settings


class Validator:
    def __init__(self, user_db: UsersCrud = Depends(get_users_crud)):
        self.settings = Depends(get_settings)

        self.user_db = user_db

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
        elif get_pass_hash(password) != user.password:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail=ErrorResponse.INVALID_PASSWORD
            )

        return True, user.id

