from unittest import TestCase
from fastapi.testclient import TestClient

from app.main import app as web_app
from app.urls import BasicUrls, UserUrls, NoteUrls


class APITestCase(TestCase):

    def setUp(self):
        self.client = TestClient(web_app)

    def test_main_url(self):
        response = self.client.get(BasicUrls.ROOT.value)
        self.assertEqual(response.status_code, 200)

    def test_create_user(self):
        user_data = dict(
            email='test_email@post.com',
            password='test123',
            nickname='test_nickname'
        )
        response = self.client.post(url=UserUrls.USER.value, json=user_data)
        self.assertEqual(response.raise_for_status(), user_data)
