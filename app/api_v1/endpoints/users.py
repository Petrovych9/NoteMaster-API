import uuid

from fastapi import Depends, HTTPException, Body, APIRouter
from starlette import status

from app.auth import check_auth_token
from app.db import get_db_session
from app.domain.users_models import UserLoginForm, UserCreateForm
from app.models import User, AuthToken
from app.domain.error_models import ErrorResponse
from app.utilts import get_pass_hash
from app.config import get_settings
from app.domain.users_crud import get_users_crud, UsersCrud

#     "email": "test1@gmail.cpom",
#     "password": "string"
users_router = APIRouter(
        prefix=get_settings().urls.users_prefix,
        tags=['users'],
    )


@users_router.post(get_settings().urls.users_endpoints.login, name='user: login')
async def login(
        user_form: UserLoginForm,
        db: UsersCrud = Depends(get_users_crud)
):
    user = db.get_by_email(user_email=user_form.email)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail=ErrorResponse.INVALID_EMAIL
        )
    # elif get_pass_hash(user_form.password) != user.password:
    elif user.password != user_form.password:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail=ErrorResponse.INVALID_PASSWORD
        )
    # auth_token = AuthToken(token=str(uuid.uuid4()), user_id=user.id)
    # try:
    #     db.add(auth_token)
    #     db.commit()
    # except Exception as e:
    #     raise HTTPException(
    #         status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
    #         detail=f"{ErrorResponse.INTERNAL_ERR0R} | {e}"
    #     )
    # return {"status": 'OK', 'auth_token': auth_token.token}
    return {"status": 'OK', 'auth_token': 'soon', 'user_id': user.id}


@users_router.post(get_settings().urls.users_endpoints.user1, name='user: create')
async def create_user(
        user_form: UserCreateForm = Body(),
        db: UsersCrud = Depends(get_users_crud)
):
    # is_user_exist = db.query(User.id).filter(
    #     User.email == user_form.email).one_or_none()
    # if is_user_exist:
    #     raise HTTPException(
    #         status_code=status.HTTP_400_BAD_REQUEST,
    #         detail=ErrorResponse.USER_ALREADY_EXIST,
    #     )
    user_id = db.create(
        email=user_form.email,
        password=user_form.password,
        nickname=user_form.nickname
    )
    if not user_id:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=ErrorResponse.INTERNAL_ERR0R
        )
    return {
        "status": status.HTTP_201_CREATED,
        "user_id": user_id
    }


@users_router.get(get_settings().urls.users_endpoints.user1, name='user: get')
async def get_user(
        token: AuthToken = Depends(check_auth_token),
        db=Depends(get_db_session)
):
    user = db.query(User).filter(User.id == token.user_id).one_or_none()
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=ErrorResponse.USER_NOT_FOUND
        )
    return {
        'id': user.id,
        'email': user.email,
        'nickname': user.nickname
    }
