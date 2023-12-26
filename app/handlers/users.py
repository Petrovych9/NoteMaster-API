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

#     "email": "test1@gmail.cpom",
#     "password": "string"
users_router = APIRouter(
        prefix=get_settings().urls.users_prefix,
        tags=['users'],
    )


@users_router.post(get_settings().urls.users_endpoints.login, name='user: login')
async def login(
        user_form: UserLoginForm,
        db=Depends(get_db_session)
):
    user = db.query(User).filter(User.email == user_form.email).one_or_none()
    if not user:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail=ErrorResponse.INVALID_EMAIL
        )
    elif get_pass_hash(user_form.password) != user.password:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail=ErrorResponse.INVALID_PASSWORD
        )
    auth_token = AuthToken(token=str(uuid.uuid4()), user_id=user.id)
    try:
        db.add(auth_token)
        db.commit()
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"{ErrorResponse.INTERNAL_ERR0R} | {e}"
        )
    return {"status": 'OK', 'auth_token': auth_token.token}


@users_router.post(get_settings().urls.users_endpoints.user1, name='user: create')
async def create_user(
        user_form: UserCreateForm = Body(),
        db=Depends(get_db_session)
):
    is_user_exist = db.query(User.id).filter(
        User.email == user_form.email).one_or_none()
    if is_user_exist:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=ErrorResponse.USER_ALREADY_EXIST,
        )
    new_user = User(
        email=user_form.email,
        password=get_pass_hash(user_form.password),
        nickname=user_form.nickname
    )

    db.add(new_user)
    db.commit()
    return {
        "status": status.HTTP_201_CREATED,
        "user_id": new_user.id
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
