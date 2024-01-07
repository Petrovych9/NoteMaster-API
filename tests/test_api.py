from unittest import TestCase

from fastapi import status
from fastapi.testclient import TestClient

from app.main import app
from app.domain.error_models import ErrorResponse
from app.config import get_settings
from app.domain.token_crud import get_token_crud, AuthTokenCrud, get_test_token_crud
from app.domain.users_crud import get_users_crud, UsersCrud, get_test_users_crud


class APITestCase(TestCase):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.settings = get_settings()
        self.api_version = self.settings.urls.api_version_prefix

        self.users_prefix = self.settings.urls.users_prefix
        self.notes_prefix = self.settings.urls.notes_prefix

        self.user_endpoints = self.settings.urls.users_endpoints
        self.notes_endpoints = self.settings.urls.notes_endpoints
        self.base_endpoints = self.settings.urls.base_endpoints

        self.users_crud: UsersCrud = get_test_users_crud()
        self.token_crud: AuthTokenCrud = get_test_token_crud()

    def setUp(self):
        app.dependency_overrides[get_users_crud] = get_test_users_crud
        app.dependency_overrides[get_token_crud] = get_test_token_crud
        self.client = TestClient(app)

    def test_main_url(self):
        response = self.client.get(self.api_version + self.base_endpoints.root)
        self.assertEqual(response.status_code, 200)

    def test_create_user(self):
        # create new user
        user_data = {
            "email": f"test_test@example.com",
            "password": "test_password1",
            "nickname": "test_nickname"
        }
        endpoint = self.user_endpoints.user1
        response = self.client.post(
            url=self.api_version + self.users_prefix + endpoint,
            json=user_data
        ).json()
        self.assertEqual(response.get('status'), status.HTTP_201_CREATED)
        self.assertIsNotNone(response.get('user_id'))

        # try to add existing user
        response = self.client.post(
            url=self.api_version + self.users_prefix + endpoint,
            json=user_data
        ).json()
        self.assertEqual(
            response.get('detail'),
            ErrorResponse.EMAIL_ALREADY_EXIST
        )

    def test_login(self):
        data = {
            "email": f"test_test@example.com",
            "password": "test_password1",
        }
        endpoint = self.user_endpoints.login
        response = self.client.post(
            url=self.api_version + self.users_prefix + endpoint,
            json=data
        ).json()
        self.assertEqual(response.get('status'), 'OK')
        self.assertIsNotNone(response.get('auth_token_id'))

        # wrong email
        data = dict(
            email="",
            password="strin$g"
        )
        response = self.client.post(
            url=self.api_version + self.users_prefix + endpoint,
            json=data
        )
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(
            response.json().get('detail'),
            ErrorResponse.INVALID_EMAIL
        )
    #
    # def test_get_user(self):
    #     new_user_id = self.users_crud.create(email='get.email', password='1111')
    #     token = self.token_crud.get_by_field(user_id=new_user_id)
    #     data = dict(token=token.token)
    #     user = self.users_crud.get_by_id(user_id=new_user_id)
    #
    #     endpoint = self.user_endpoints.user1
    #     response = self.client.get(
    #         url=self.api_version + self.users_prefix + endpoint,
    #         params=data
    #     ).json()
    #
    #     self.assertEqual(response.get('id'), user.id)
    #     self.assertEqual(response.get('email'), user.email)
    #     self.assertEqual(response.get('nickname'), user.nickname)
    #

