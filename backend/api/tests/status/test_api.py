"""
Test Status APIs
"""

from django.test import TestCase, SimpleTestCase
from rest_framework.test import RequestsClient, APITestCase
from django.core.management import call_command
from rest_framework import status
from uuid import uuid4


from ...models import *
from django.contrib.auth.models import User


class StatusAPITests(APITestCase):
    """
    Test for User status API endpoints
    """

    GET_TOKEN_URL = "http://127.0.0.1:8000/api/token/"

    BASE_URL = "http://127.0.0.1:8000/api"

    def setUp(self) -> None:
        # pass
        call_command("seed_db")

    def tearDown(self) -> None:
        # pass
        call_command("clear_db")

    def authenticate(self, username, password):
        response = self.client.post(
            path=self.GET_TOKEN_URL,
            data={
                "username": username,
                "password": password,
            },
            format="json",
        )

        return response.data.get("access")

    def test_authenticated_request_return_200(self):
        """
        Test authenticated API request with correct payload returns 200 OK
        Test Pass criteria:
            - Make a POST /api/users/status and provide bearer token and payload
            - Pass if response status code = 200
        """
        random_user = User.objects.first()
        random_user_username = random_user.username
        random_user_password = random_user.username

        ACCESS_TOKEN = self.authenticate(random_user_username, random_user_password)

        headers = {"Authorization": f"Bearer {ACCESS_TOKEN}"}

        body = {"username": random_user_username, "status": "dnd"}

        response = self.client.patch(
            self.BASE_URL + "/users/status", body, headers=headers, format="json"
        )

        self.assertEqual(response.status_code, 200)

    def test_unauthenticated_request_return_401(self):
        """
        Test unauthenticated API request with correct payload returns 401 OK
        Test Pass criteria:
            - Make a POST /api/users/status and provide incorrect bearer token and payload
            - Pass if response status code = 401

        """
        random_user = User.objects.first()
        random_user_username = random_user.username
        random_user_password = random_user.username

        ACCESS_TOKEN = self.authenticate(random_user_username, random_user_password)

        headers = {"Authorization": f"Bearer {ACCESS_TOKEN}extra"}

        body = {"username": random_user_username, "status": "dnd"}

        response = self.client.patch(
            self.BASE_URL + "/users/status", body, headers=headers, format="json"
        )

        self.assertEqual(response.status_code, 401)
