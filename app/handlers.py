import uuid

from fastapi import APIRouter, Body, Depends, HTTPException  # todo what is it
from starlette import status

from app.forms import UserLoginForm, UserCreateForm
from app.models import connect_db, User, AuthToken

from app.auth import check_auth_token
from app.utilts import get_pass_hash

auth_router = APIRouter()  # todo what is it


@auth_router.post('/login', name='user: login')
async def login(
        user_form: UserLoginForm = Body(..., embed=True),
        db=Depends(connect_db)
):
    user = db.query(User).filter(User.email == user_form.email).one_or_none()
    if not user or get_pass_hash(user_form.password) != user.password:
        return 500

    auth_token = AuthToken(token=str(uuid.uuid4()), user_id=user.id)
    db.add(auth_token)
    db.commit()
    return {"status": 'OK', 'auth_token': auth_token.token}


#     "email": "test1@gmail.cpom",
#     "password": "string"

@auth_router.post('/user', name='user: create')
async def create_user(
        user_form: UserCreateForm = Body(..., embed=True),
        db=Depends(connect_db)
):
    is_user_exist = db.query(User.id).filter(
        User.email == user_form.email).one_or_none()
    if is_user_exist:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail='User already exist',
        )
    new_user = User(
        email=user_form.email,
        password=get_pass_hash(user_form.password),
        nickname=user_form.nickname
    )

    db.add(new_user)
    db.commit()
    return {
        "status": 'OK',
        "user_id": new_user.id
    }


@auth_router.get('/user', name='user: get')
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


@auth_router.get('/', name='root')
def root():
    return status.HTTP_200_OK
