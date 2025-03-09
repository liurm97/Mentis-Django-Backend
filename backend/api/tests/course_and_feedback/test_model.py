"""
Test Course data model
"""

from django.test import TestCase
from ...models import Course, CourseTracker, StudentFeedback
from django.contrib.auth.models import User
from django.db.utils import IntegrityError
from uuid import uuid4
from django.core.exceptions import ValidationError
from django.db import transaction


class CourseModelTests(TestCase):
    """
    Test for Course, CourseTracker, StudentFeedback model
    """

    random_pwd = str(uuid4())

    create_user_obj = {
        "username": "test123",
        "first_name": "test",
        "last_name": "123",
        "password": random_pwd,
    }

    create_course_obj = {
        "name": "101 ways to make million dollars in a year",
        "category": "business",
        "subcategory": "sales",
        "description": "Course is to teach students ways to make a million dollar in one year",
    }

    def setUp(self) -> None:
        # setup before every test
        User.objects.create(**self.create_user_obj)

    def tearDown(self) -> None:
        # teardown after every test
        User.objects.all().delete()

    def test_insert_into_course_table_should_succeed_with_valid_course_data(
        self,
    ):
        """
        Test insert into Course table should succeed with valid data
        Test Pass criteria:
            - Get random existing user in Users table
            - Get course enrolled by the existing user
            - Get a feedback left by the existing user
            - Provide name = "101 ways to make million dollars in a year"
            - Provide category = "business"
            - Provide subcategory = "sales"
            - Provide description = "Course is to teach students ways to make a million dollar in one year"
            - After insert, lookup existing user against CourseTracker table and validate the existing user is returned
        """
        random_user = User.objects.first()

        created_course = Course.objects.create(**self.create_course_obj)

        CourseTracker.objects.create(
            user=random_user, course=created_course, profile="learner"
        )

        StudentFeedback.objects.create(
            student=random_user,
            course=created_course,
            feedback="This is a good course!",
        )

        self.assertEqual(
            CourseTracker.objects.filter(user=random_user)[0].user.username,
            random_user.username,
        )

    def test_insert_into_coursetracker_table_should_fail_with_invalid_profile_data(
        self,
    ):
        """
        Test insert into CourseTracker table should fail with invalid profile data
        Test Pass criteria:
            - Get random existing user in Users table
            - Get course enrolled by the existing user
            - Validate IntegrityError is raised while inserting into CourseTracker table
        """
        random_user = User.objects.first()

        created_course = Course.objects.create(**self.create_course_obj)

        with self.assertRaises(IntegrityError):

            # run atomic transaction to correctly evaluate test
            with transaction.atomic():
                CourseTracker.objects.create(
                    user=random_user, course=created_course, profile="learning"
                )

                StudentFeedback.objects.create(
                    student=random_user,
                    course=created_course,
                    feedback="This is a good course!",
                )
