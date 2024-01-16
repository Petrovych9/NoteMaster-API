from typing import Annotated

from fastapi import Depends, HTTPException, Body, APIRouter, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm

from app.domain.users_models import UserCreateForm
from app.domain.error_models import ErrorResponse
from app.domain.users_crud import get_users_crud, UsersCrud
from app.domain.token_crud import AuthTokenCrud, get_token_crud
from app.domain.auth_models import TokenInfo
from app.domain.auth import JwtToken
from app.domain.validation import Validator, get_validator
from app.utilts import get_pass_hash
from app.config import get_settings, Settings


users_router = APIRouter(
        prefix=get_settings().urls.users_prefix,
        tags=['users'],
    )

oauth_scheme = OAuth2PasswordBearer(
    tokenUrl=f"{get_settings().urls.users_endpoints.get_url(
        endpoint=get_settings().urls.users_endpoints.login
    )}"
)


@users_router.post(get_settings().urls.users_endpoints.login, name='user: login (get jwt)')
async def login(
        user_form: Annotated[OAuth2PasswordRequestForm, Depends()],
        token_db: AuthTokenCrud = Depends(get_token_crud),
        settings: Settings = Depends(get_settings),
        jwt: JwtToken = Depends(JwtToken),
        validator: Validator = Depends(Validator),
):
    hashed_pass = get_pass_hash(user_form.password)

    is_valid, user_id = validator.check_user(
        email=user_form.username,
        password=hashed_pass
    )
    if not is_valid:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail=ErrorResponse.USER_NOT_FOUND
        )

    token = jwt.encode(
        payload=dict(
            email=user_form.username,
            password=hashed_pass
        )
    )
    refresh_token = jwt.encode(
        payload=dict(
            email=user_form.username,
            password=hashed_pass
        ),
        life_time_sec=settings.jwt.long_life_time_sec
    )
    print(token)
    print('refresh:  ', refresh_token)
    if not token or not refresh_token:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=ErrorResponse.INTERNAL_ERR0R
        )

    auth_token_id = token_db.create(token=refresh_token, user_id=user_id)
    if not auth_token_id:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=ErrorResponse.INTERNAL_ERR0R
        )

    return TokenInfo(access_token=token, refresh_token=refresh_token)


@users_router.post(get_settings().urls.users_endpoints.refresh_token, name='refresh access token')
def refresh_access_token(
        refresh_token: str,
        token_db: AuthTokenCrud = Depends(get_token_crud),
        settings: Settings = Depends(get_settings),
        jwt: JwtToken = Depends(JwtToken),
        validator: Validator = Depends(Validator),
):
    auth_token, payload = validator.check_auth_token(token=refresh_token)

    is_valid_user, user_id = validator.check_user(
        email=payload.get('email'),
        password=payload.get('password')
    )
    if not auth_token or not is_valid_user:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail=ErrorResponse.USER_NOT_FOUND
        )

    new_token = jwt.encode(
        payload=dict(
            email=payload.get('email'),
            password=payload.get('password'),
        ),
        life_time_sec=settings.jwt.long_life_time_sec
    )

    auth_token_id = token_db.create(token=new_token, user_id=user_id)
    if not auth_token_id:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=ErrorResponse.INTERNAL_ERR0R
        )

    return TokenInfo(access_token=new_token, refresh_token=refresh_token)
# todo need to link each refresh to each user and do not create always new token

@users_router.post(get_settings().urls.users_endpoints.user1, name='user: create')
async def create_user(
        user_form: UserCreateForm = Body(),
        user_db: UsersCrud = Depends(get_users_crud)
):
    is_user_exist = user_db.get_by_email(user_email=user_form.email)
    if is_user_exist:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=ErrorResponse.EMAIL_ALREADY_EXIST,
        )
    user_id = user_db.create(
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
        token: str = Depends(oauth_scheme),
        user_db: UsersCrud = Depends(get_users_crud),
        token_db: AuthTokenCrud = Depends(get_token_crud),
        validator: Validator = Depends(get_validator),
):
    token, is_valid = validator.check_auth_token(token=str(token))

    if not is_valid or not token:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail=ErrorResponse.INVALID_TOKEN
        )

    user = user_db.get_by_id(
        user_id=token_db.get_by_field(token=token.token).user_id
    )
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
