
from fastapi import Depends, HTTPException, Body, APIRouter, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials, \
    OAuth2PasswordBearer

from app.domain.users_models import UserLoginForm, UserCreateForm
from app.models import AuthToken
from app.domain.error_models import ErrorResponse
from app.utilts import get_pass_hash
from app.config import get_settings, Settings
from app.domain.users_crud import get_users_crud, UsersCrud
from app.domain.token_crud import AuthTokenCrud, get_token_crud
from app.domain.auth_models import TokenInfo
from app.domain.auth import JwtToken
from app.domain.validation import Validator


#     "email": "test1@gmail.cpom",
#     "password": "string"
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
        user_form: UserLoginForm,
        token_db: AuthTokenCrud = Depends(get_token_crud),
        settings: Settings = Depends(get_settings),
        jwt: JwtToken = Depends(JwtToken),
        validator: Validator = Depends(Validator),
):
    hashed_pass = get_pass_hash(user_form.password)

    is_valid, user_id = validator.check_user(
        email=user_form.email,
        password=hashed_pass
    )

    token = jwt.encode(
        payload=dict(
            email=user_form.email,
            password=hashed_pass
        )
    )

    auth_token_id = token_db.create(token=token, user_id=user_id)
    if not auth_token_id:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"{ErrorResponse.INTERNAL_ERR0R}"
        )

    return TokenInfo(access_token=token, token_type=settings.jwt.type), user_id


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
        token: AuthToken = Depends(Validator().check_auth_token),
        user_db: UsersCrud = Depends(get_users_crud),
        token_db: AuthTokenCrud = Depends(get_token_crud)
):
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
