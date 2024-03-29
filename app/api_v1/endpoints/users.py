from typing import Annotated

from fastapi import Depends, HTTPException, APIRouter, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm

from app.domain.users import users_models as m
from app.domain.base_models import ErrorResponse
from app.domain.users.users_crud import get_users_crud, UsersCrud
from app.domain.auth.token_crud import AuthTokenCrud, get_token_crud
from app.domain.auth.auth import JwtToken
from app.domain.validation import Validator
from app.domain.users.utilts import get_pass_hash
from app.config import get_settings, Settings
from app.domain.helper import Helper, get_helper


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

    token, _ = jwt.encode(
        payload=dict(
            email=user_form.username,
            password=hashed_pass
        )
    )
    refresh_token, expire = jwt.encode(
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

    auth_token = token_db.update(
        field_value=dict(token=refresh_token, expire=expire),
        user_id=user_id
    )
    if not auth_token:
        auth_token_id = token_db.create(
            token=refresh_token,
            user_id=user_id,
            expire=expire
        )
        if not auth_token_id:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=ErrorResponse.INTERNAL_ERR0R
            )

    return m.RefreshAccessTokenResponse(access_token=token, refresh_token=refresh_token)


@users_router.post(get_settings().urls.users_endpoints.refresh_token, name='refresh access token')
def refresh_access_token(
        data: m.RefreshAccessTokenRequest,
        token_db: AuthTokenCrud = Depends(get_token_crud),
        settings: Settings = Depends(get_settings),
        jwt: JwtToken = Depends(JwtToken),
        validator: Validator = Depends(Validator),
):
    auth_token, payload = validator.check_auth_token(token=data.refresh_token)

    is_valid_user, user_id = validator.check_user(
        email=payload.get('email'),
        password=payload.get('password')
    )
    if not auth_token or not is_valid_user:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail=ErrorResponse.USER_NOT_FOUND
        )

    new_access_token, _ = jwt.encode(
        payload=dict(
            email=payload.get('email'),
            password=payload.get('password'),
        ),
    )
    if data.update_refresh_token:
        new_refresh_token, expire = jwt.encode(
            payload=dict(
                email=payload.get('email'),
                password=payload.get('password'),
            ),
            life_time_sec=settings.jwt.long_life_time_sec
        )

        auth_token_id = token_db.update(
            field_value=dict(token=new_refresh_token, expire=expire),
            user_id=user_id
        )
        if not auth_token_id:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=ErrorResponse.INTERNAL_ERR0R
            )
        return m.RefreshAccessTokenResponse(access_token=new_access_token, refresh_token=new_refresh_token)

    return m.RefreshAccessTokenResponse(
        access_token=new_access_token,
        refresh_token=data.refresh_token
    )


@users_router.post(get_settings().urls.users_endpoints.user1, name='user: create')
async def create_user(
        user_form: m.CreateUserRequest,
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
    return m.CreateUserResponse(user_id=user_id)


@users_router.get(get_settings().urls.users_endpoints.user1, name='user: get')
async def get_user(
        token: str = Depends(oauth_scheme),
        helper: Helper = Depends(get_helper)
):
    user = helper.get_current_user(token)
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
    return m.GetUserResponse(
        user_id=user.id,
        email=user.email,
        nickname=user.nickname
    )
