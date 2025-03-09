"""
Test Custom management command
"""

from django.test import TestCase
from django.core.management import call_command

from ...models import *


class EventsAPITests(TestCase):
    """
    Test custom management commands created to seed and clear db
    """

    def setUp(self) -> None:
        call_command("seed_db")

    def tearDown(self) -> None:
        call_command("clear_db")

    def test_seed_db_create_5_users_and_15_courses(self):
        """
        Test seed_db custom command creates 5 users and 15 courses
        """
        num_users = len(User.objects.all())
        num_courses = len(Course.objects.all())
        expect = [num_users, num_courses]
        self.assertEqual(expect, [5, 15])
