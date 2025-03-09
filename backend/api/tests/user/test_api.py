"""
Test User APIs
"""

from django.test import TestCase, SimpleTestCase
from rest_framework.test import RequestsClient, APITestCase
from django.core.management import call_command
from django.db.utils import IntegrityError
from rest_framework import status
from uuid import uuid4

from ...models import Role
from django.contrib.auth.models import User


class RegisterUserAPITests(APITestCase):
    """
    Test for Reigster User API endpoints
    """

    BASE_URL = "http://127.0.0.1:8000/api/user/register/"

    valid_register_user_payload = {
        "username": "test123",
        "first_name": "test",
        "last_name": "123",
        "role": "teacher",
        "email": "test123@gmail2.com",
        "password": "test123",
    }

    def setUp(self) -> None:
        pass
        # seed_db_dates()

    def tearDown(self) -> None:
        pass
        # Event.objects.all().delete()

    def test_register_student_user_success_returns_201(self):
        """
        Test register user successfully returns 201 OK
        Test Pass criteria:
            - Make a POST /api/v1/register and provide valid payload = student
            - Pass if response status code = 201
        """
        valid_register_user_payload = {
            "username": "test123",
            "first_name": "test",
            "last_name": "123",
            "role": "student",
            "email": "test1@gmail.com",
            "password": "test123",
        }

        response = self.client.post(
            self.BASE_URL, valid_register_user_payload, format="json"
        )

        self.assertEqual(response.status_code, 201)

    def test_register_teacher_user_success_returns_201(self):
        """
        Test register user successfully returns 201 OK
        Test Pass criteria:
            - Make a POST /api/v1/register and provide valid payload = teacher
            - Pass if response status code = 201
        """

        response = self.client.post(
            self.BASE_URL, self.valid_register_user_payload, format="json"
        )

        self.assertEqual(response.status_code, 201)

    def test_register_user_with_duplicate_username_returns_400(self):
        """
        Test register user with duplicate username returns 400 BAD REQUEST
        Test Pass criteria:
            - Make a POST /api/v1/register and provide duplicate username
            - Pass if response status code = 400
        """

        expected_responses = [201, 400]
        actual_responses = []

        for i in range(2):

            # same username is used twice
            response = self.client.post(
                self.BASE_URL, self.valid_register_user_payload, format="json"
            )
            actual_responses.append(response.status_code)

            # update email so that email is unique
            self.valid_register_user_payload["email"] = "test2@gmail.com"

        self.assertListEqual(actual_responses, expected_responses)

    def test_register_user_with_duplicate_email_returns_400(self):
        """
        Test register user with duplicate email returns 400 BAD REQUEST
        Test Pass criteria:
            - Make a POST /api/v1/register and provide duplicate email
            - Pass if response status code = 400
        """

        expected_responses = [201, 400]
        actual_responses = []

        for i in range(2):

            # same email is used twice
            response = self.client.post(
                self.BASE_URL, self.valid_register_user_payload, format="json"
            )
            actual_responses.append(response.status_code)

            # update username so that username is unique
            self.valid_register_user_payload["username"] = "test321"

        self.assertListEqual(actual_responses, expected_responses)

    def test_register_user_with_invalid_role_returns_400(self):
        """
        Test register user with invalid role returns 400 BAD REQUEST
        Test Pass criteria:
            - Make a POST /api/v1/register and provide invalid role
            - Pass if response status code = 400
        """

        invalid_role = "studen"

        self.valid_register_user_payload["role"] = invalid_role

        response = self.client.post(
            self.BASE_URL, self.valid_register_user_payload, format="json"
        )

        self.assertEqual(response.status_code, 400)
