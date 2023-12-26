from unittest import TestCase
from bson import ObjectId

from fastapi import status
from fastapi.testclient import TestClient

from app.db import get_db_session, override_get_db_session
from app.main import app
from app.domain.error_models import ErrorResponse
from app.config import get_settings


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

    def setUp(self):
        app.dependency_overrides[get_db_session] = override_get_db_session
        self.client = TestClient(app)

    def __fetch_response(self, endpoint: str, prefix: str, data: dict):
        return self.client.post(
            url=self.api_version + prefix + endpoint,
            json=data
        )# TODO rebuild all according to this fetch

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
            ErrorResponse.USER_ALREADY_EXIST
        )

    def test_get_user(self):
        # Ask for non existing user
        data = dict(token='17cca16a-87d6-42ss55-bc0c-bc830e73c8b8')
# todo need to create crud for user
        endpoint = self.user_endpoints.user1
        response = self.client.get(
            url=self.api_version + self.users_prefix + endpoint,
            params=data
        )
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)  # wrong token
        # response = response.json()
        # self.assertIsNotNone(response.get('id'))
        # self.assertIsNotNone(response.get('email'))
        # self.assertIsNotNone(response.get('nickname'))

    def test_login(self):
        data = {
            "email": f"test_test@example.com",
            "password": "test_password1",
            "nickname": "test_nickname"
        }
        endpoint = self.user_endpoints.login
        response = self.client.post(
            url=self.api_version + self.users_prefix + endpoint,
            json=data
        ).json()
        self.assertEqual(response.get('status'), 'OK')
        self.assertIsNotNone(response.get('auth_token'))

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
