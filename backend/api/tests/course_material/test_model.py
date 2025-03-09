"""
Test Course Material data model

** Pending more information to determine format of uploadURL **
- may consider adding regex validator, etc
"""

from django.test import TestCase
from ...models import Course, CourseMaterial
from django.contrib.auth.models import User
from django.db.utils import IntegrityError
from uuid import uuid4
from django.core.exceptions import ValidationError
from django.db import transaction


class CourseMaterialModelTests(TestCase):
    """
    Test for Course Material model
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
        Course.objects.create(**self.create_course_obj)

    def tearDown(self) -> None:
        # teardown after every test
        User.objects.all().delete()
        Course.objects.all().delete()

    def test_insert_into_course_material_table_should_succeed_with_valid_data(
        self,
    ):
        """
        Test insert into CourseMaterial table should succeed with valid data
        Test Pass criteria:
            - Get random course from Course table
            - Provide valid data
            - After insert, validate size of CourseMaterial table = 1
        """
        random_course = Course.objects.first()

        course_material_payload = {
            "title": "introduction",
            "content": "introduction content",
            "duration": 20,
        }

        CourseMaterial.objects.create(**course_material_payload, course=random_course)

        num_course_materials_records = len(CourseMaterial.objects.all())
        self.assertEqual(num_course_materials_records, 1)
