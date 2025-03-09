"""
Test Status data model
"""

from django.test import TestCase
from ...models import Status
from django.contrib.auth.models import User
from django.db.utils import IntegrityError
from uuid import uuid4
from django.core.exceptions import ValidationError
from django.db import transaction


class StatusModelTests(TestCase):
    """
    Test for Status model
    """

    random_pwd = str(uuid4())

    create_user_obj = {
        "username": "test123",
        "first_name": "test",
        "last_name": "123",
        "password": random_pwd,
    }

    def setUp(self) -> None:
        # setup before every test
        User.objects.create(**self.create_user_obj)

    def tearDown(self) -> None:
        # teardown after every test
        User.objects.all().delete()

    def test_insert_into_status_table_should_succeed_with_valid_role_data_one(self):
        """
        Test insert into status table should succeed with valid data
        Test Pass criteria:
            - Get random existing user in Users table
            - Provide status data = active
            - After insert, validate size of role table = 1
        """
        random_user = User.objects.first()

        Status.objects.create(status="active", userStatus=random_user)

        num_role_records = len(Status.objects.all())
        self.assertEqual(num_role_records, 1)

    def test_insert_into_status_table_should_succeed_with_valid_role_data_two(self):
        """
        Test insert into status table should succeed with valid data
        Test Pass criteria:
            - Get random existing user in Users table
            - Provide status data = busy
            - After insert, validate size of role table = 1
        """
        random_user = User.objects.first()

        Status.objects.create(status="busy", userStatus=random_user)

        num_role_records = len(Status.objects.all())
        self.assertEqual(num_role_records, 1)

    def test_insert_into_status_table_should_succeed_with_valid_role_data_three(self):
        """
        Test insert into status table should succeed with valid data
        Test Pass criteria:
            - Get random existing user in Users table
            - Provide status data = dnd
            - After insert, validate size of role table = 1
        """
        random_user = User.objects.first()

        Status.objects.create(status="dnd", userStatus=random_user)

        num_role_records = len(Status.objects.all())
        self.assertEqual(num_role_records, 1)

    def test_insert_into_status_table_should_succeed_with_valid_role_data_four(self):
        """
        Test insert into status table should succeed with valid data
        Test Pass criteria:
            - Get random existing user in Users table
            - Provide status data = away
            - After insert, validate size of role table = 1
        """
        random_user = User.objects.first()

        Status.objects.create(status="away", userStatus=random_user)

        num_role_records = len(Status.objects.all())
        self.assertEqual(num_role_records, 1)

    def test_insert_into_status_table_should_fail_with_invalid_role_data(self):
        """
        Test insert into status table should fail with invalid role data
        Test Pass criteria:
            - Get random existing user in Users table
            - Provide invalid role data = offline
            - After insert, validate size of role table = 1
        """
        random_user = User.objects.first()

        with self.assertRaises(IntegrityError):
            # run atomic transaction to correctly evaluate test
            with transaction.atomic():
                Status.objects.create(status="offline", userStatus=random_user)
