from unittest import TestCase
from fastapi.testclient import TestClient

from app.main import app as web_app


class APITestCase(TestCase):

    def setUp(self):
        self.client = TestClient(web_app)

    def test_main_url(self):
        response = self.client.get('/')
        self.assertEqual(response.status_code, 200)

    def test_create_user(self):
        user_data = dict(
            email='test_email@post.com',
            password='test123',
            nickname='test_nickname'
        )
        response = self.client.post(url='/user', json=user_data)
        self.assertIsNotNone(response.json())
