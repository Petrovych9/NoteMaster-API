from unittest import TestCase
from fastapi.testclient import TestClient
from fastapi import status
from bson import ObjectId

from app.main import app as web_app
from app.urls import BasicUrls, UserUrls, NoteUrls


class APITestCase(TestCase):

    def setUp(self):
        self.client = TestClient(web_app)

    def test_main_url(self):
        response = self.client.get(BasicUrls.ROOT.value)
        self.assertEqual(response.status_code, 200)

    def test_create_user(self):
        # try to add existing user
        user_data = {
            "email": "test@example.com",
            "password": "test_password",
            "nickname": "test_nickname"
        }

        response = self.client.post(url=UserUrls.USER.value,
                                    json=user_data).json()
        self.assertEqual(response.get('detail'), "User already exist")

        # create new user
        user_data = {
            "email": f"test_test{ObjectId()}@example.com",
            "password": "test_password1",
            "nickname": "test_nickname"
        }

        response = self.client.post(
            url=UserUrls.USER.value,
            json=user_data
        ).json()
        print(response)
        self.assertEqual(response.get('status'), status.HTTP_201_CREATED)
        self.assertIsNotNone(response.get('user_id'))

    def test_get_user(self):
        data = dict(token='17cca16a-87d6-4255-bc0c-bc830e73c8b8')

        response = self.client.get(url=UserUrls.USER.value, params=data)
        self.assertEqual(response.status_code, 200)
        response = response.json()
        self.assertIsNotNone(response.get('id'))
        self.assertIsNotNone(response.get('email'))
        self.assertIsNotNone(response.get('nickname'))

    def test_login(self):
        data = dict(
            email="test1@gmail.cpom",
            password="string"
        )
        response = self.client.post(
            url=BasicUrls.LOGIN.value,
            json=data
        ).json()
        self.assertEqual(response.get('status'), 'OK')
        self.assertIsNotNone(response.get('auth_token'))

        # wrong email
        data = dict(
            email="",
            password="strin$g"
        )
        response = self.client.post(url=BasicUrls.LOGIN.value, json=data)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            response.json(),
            status.HTTP_500_INTERNAL_SERVER_ERROR
        )
