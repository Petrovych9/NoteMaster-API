from unittest import TestCase
from bson import ObjectId

from fastapi import status
from fastapi.testclient import TestClient

from app.db import get_db_session, override_get_db_session
from app.main import app
from app.models import ErrorResponse
from app.urls import BasicUrls, UserUrls, NoteUrls


class APITestCase(TestCase):
    api = '/v1/'
    users = 'users'   # todo create normal urls, centralizeted

    def setUp(self):
        app.dependency_overrides[get_db_session] = override_get_db_session
        self.client = TestClient(app)

    def test_main_url(self):
        response = self.client.get(self.api)
        self.assertEqual(response.status_code, 200)

    def test_create_user(self):
        # create new user
        user_data = {
            "email": f"test_test@example.com",
            "password": "test_password1",
            "nickname": "test_nickname"
        }
        print(self.api + self.users + UserUrls.USER.value)
        response = self.client.post(
            url=self.api + self.users + UserUrls.USER.value,
            json=user_data
        ).json()
        self.assertEqual(response.get('status'), status.HTTP_201_CREATED)
        self.assertIsNotNone(response.get('user_id'))

        # try to add existing user
        response = self.client.post(
            url=self.api + self.users + UserUrls.USER.value,
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
        response = self.client.get(url=self.api + self.users + UserUrls.USER.value, params=data)
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
        response = self.client.post(
            url=self.api + self.users + BasicUrls.LOGIN.value,
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
            url=self.api + self.users + BasicUrls.LOGIN.value,
            json=data
        )
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(
            response.json().get('detail'),
            ErrorResponse.INVALID_EMAIL
        )
