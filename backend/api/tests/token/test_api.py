"""
Test SimpleJWT APIs
"""

from django.test import TestCase, SimpleTestCase
from rest_framework.test import APITestCase
from django.db.utils import IntegrityError
from rest_framework import status
from uuid import uuid4
import jwt
from dotenv import load_dotenv
import os

from ...models import Role
from django.contrib.auth.models import User


class SimpleJWTAPITests(APITestCase):
    """
    Test for SimpleJWT API endpoints
    """

    BASE_CREATE_TOKEN_URL = "http://127.0.0.1:8000/api/token/"
    BASE_REFRESH_TOKEN_URL = "http://127.0.0.1:8000/api/token/refresh/"

    user_payload = {
        "username": "test12345",
        "first_name": "test",
        "last_name": "12345",
        "email": "test12345@gmail.com",
        "role": "teacher",
        "password": "test12345",
    }

    def setUp(self) -> None:
        pass

    def tearDown(self) -> None:
        pass

    def test_create_token_success_returns_custom_role_claim(self):
        """
        Test create token returns token containing custom role claim
        Test Pass criteria:
            - Make a POST /api/token/ and provide valid user credential
            - Decode access token
            - Pass if token contains `role` key
        """
        role = self.user_payload.pop("role")
        created_user = User.objects.create_user(**self.user_payload)
        Role.objects.create(role=role, userRole=created_user)

        username = created_user.username
        password = self.user_payload.get("password")

        data = {"username": username, "password": password}

        response = self.client.post(
            self.BASE_CREATE_TOKEN_URL, data=data, format="json"
        )

        json_response = response.json()
        access_token = json_response.get("access")

        jwt_secret = os.getenv("SECRET")
        decoded = jwt.decode(access_token, jwt_secret, algorithms="HS256")

        self.assertEqual(decoded.get("role"), role)
