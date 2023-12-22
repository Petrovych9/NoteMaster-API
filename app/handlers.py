import uuid

from fastapi import APIRouter, Body, Depends, HTTPException  # todo what is it
from fastapi import status

from app.forms import UserLoginForm, UserCreateForm
from app.models import connect_db, User, AuthToken, ErrorResponse
from app.urls import BasicUrls, UserUrls, NoteUrls
from app.auth import check_auth_token
from app.utilts import get_pass_hash

auth_router = APIRouter()  # todo what is it


@auth_router.post(BasicUrls.LOGIN.value, name='user: login')
async def login(
        user_form: UserLoginForm,
        db=Depends(connect_db)
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


#     "email": "test1@gmail.cpom",
#     "password": "string"

@auth_router.post(UserUrls.USER.value, name='user: create')
async def create_user(
        user_form: UserCreateForm,
        db=Depends(connect_db)
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


@auth_router.get(UserUrls.USER.value, name='user: get')
async def get_user(
        token: AuthToken = Depends(check_auth_token),
        db=Depends(connect_db)
):
    user = db.query(User).filter(User.id == token.user_id).one_or_none()
    return {
        'id': user.id,
        'email': user.email,
        'nickname': user.nickname
    }


@auth_router.get(BasicUrls.ROOT.value, name='root')
def root():
    return status.HTTP_200_OK
