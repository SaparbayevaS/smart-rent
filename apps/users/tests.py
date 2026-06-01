from django.contrib.auth import get_user_model
from rest_framework.test import APITestCase

User = get_user_model()


class AuthTests(APITestCase):
    def setUp(self) -> None:
        self.register_url = "/api/users/register/"
        self.login_url = "/api/users/login/"

        self.user_data = {
            "email": "test@test.com",
            "password": "test12345678",
        }

    def test_register_user(self) -> None:
        response = self.client.post(
            self.register_url,
            self.user_data,
        )
        self.assertIn(
            response.status_code,
            [200, 201],
        )

    def test_login_user(self) -> None:
        User.objects.create_user(
            email="test@test.com",
            password="test12345678",
        )

        response = self.client.post(
            self.login_url,
            self.user_data,
        )

        self.assertEqual(
            response.status_code,
            200,
        )
        self.assertIn(
            "access",
            response.data,
        )

    def test_login_invalid_user(self) -> None:
        response = self.client.post(
            self.login_url,
            {
                "email": "wrong@test.com",
                "password": "wrong",
            },
        )

        self.assertIn(
            response.status_code,
            [400, 401],
        )