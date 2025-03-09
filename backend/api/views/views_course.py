import os
from uuid import uuid4
from django.contrib.auth.models import User
import jwt
from rest_framework import generics
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.exceptions import ValidationError
from ..serializers.serializers_course import (
    AddCourseReviewSerializer,
    ListCoursesSerializer,
    CreateCourseSerializer,
    RemoveStudentFromCourseSerializer,
    UpdateCourseUserBlockStatusSerializer,
)
from django.db.utils import IntegrityError
from rest_framework import serializers
from api.models import Course, CourseTracker, StudentFeedback, CourseMaterial, Role
from django.db.models import Q
from datetime import datetime
import pytz
from django.utils import timezone
from django.db import transaction


class ListCousesByCategoryView(APIView):
    """
    Public route - List courses by course category

    Params:
    @category - Required parameter to filter course
    @limit - Optional parameter to return x number of courses
    """

    # Allow any access
    permission_classes = [AllowAny]

    def post(self, request, format=None):
        data = request.data
        category = data.get("category")
        limitExists = False
        if "limit" in data:
            limitExists = True
            raw_limit = data.get("limit")

        serializer = ListCoursesSerializer(data=request.data)
        try:
            if serializer.is_valid():
                category = serializer.validated_data.get("category")

                # if `limit` is provided in request body
                if limitExists:
                    validated_limit = serializer.validated_data.get("limit")
                    courses = list(
                        Course.objects.filter(category=category).values_list(
                            "name", "subcategory", "id"
                        )
                    )[:validated_limit]
                else:
                    courses = list(
                        Course.objects.filter(category=category).values_list(
                            "name", "subcategory", "id"
                        )
                    )

                formatted_courses = {"category": category, "courses": []}

                for course in courses:
                    name, subcategory, id = course

                    author = CourseTracker.objects.get(
                        Q(course_id=id) & Q(profile="author")
                    )
                    author_first_name = author.user.first_name
                    author_last_name = author.user.last_name

                    formatted_courses.get("courses").append(
                        {
                            "name": name,
                            "subcategory": subcategory,
                            "author": f"{author_first_name} {author_last_name}",
                            "id": id,
                        }
                    )

                return Response(
                    formatted_courses,
                    status=status.HTTP_200_OK,
                )

            else:
                return Response(
                    serializer.errors,
                    status=status.HTTP_400_BAD_REQUEST,
                )

        except serializers.ValidationError as e:
            return Response(
                e.detail,
                status=status.HTTP_400_BAD_REQUEST,
            )


class ListCourseDetailView(APIView):
    """
    Public route - List course details, author, enrolled_students, course_feedback, course_materials
    """

    # Allow any access
    permission_classes = [AllowAny]

    def convert_to_localtime(self, utctime):
        fmt = "%b %d, %Y"
        utc = utctime.replace(tzinfo=pytz.UTC)
        localtz = utc.astimezone(timezone.get_current_timezone())
        return localtz.strftime(fmt)

    def validate_course_id(self, course_id: str) -> bool:
        if course_id in list(Course.objects.values_list("id", flat=True)):
            return True
        return False

    def get(self, request, course_id):

        if not self.validate_course_id(course_id=course_id):
            return Response(
                f"The course_id you provided ({course_id}) does not exist.",
                status=status.HTTP_400_BAD_REQUEST,
            )

        try:

            # Course details
            course_name, course_category, course_subcategory, course_description = (
                Course.objects.filter(id=course_id).values_list(
                    "name", "category", "subcategory", "description"
                )[0]
            )

            # Author
            author = CourseTracker.objects.get(
                Q(course_id=course_id) & Q(profile="author")
            )
            author_username = author.user.username
            author_first_name = author.user.first_name
            author_last_name = author.user.last_name

            # Enrolled students
            enrolled_student_list = []
            enrolled_students = CourseTracker.objects.filter(
                Q(course_id=course_id) & Q(profile="learner")
            ).values("user", "is_blocked", "created_at")

            for student in enrolled_students:
                student_id = student.get("user")
                enrolled_date_utc = student.get("created_at")
                enrolled_date_local = self.convert_to_localtime(enrolled_date_utc)
                is_blocked = student.get("is_blocked")
                student = User.objects.get(id=student_id)
                student_username = student.username
                student_fullname = f"{student.first_name} {student.last_name}"
                enrolled_student_list.append(
                    {
                        "id": student_id,
                        "username": student_username,
                        "name": student_fullname,
                        "is_blocked": is_blocked,
                        "enrolled_date": enrolled_date_local,
                    }
                )

            # Student feedback
            feedback_list = []
            feedbacks = StudentFeedback.objects.filter(course__id=course_id)
            feedback_count = len(feedbacks)

            if feedback_count > 0:
                for feedback in feedbacks:
                    feedback_provided_by_student_full_name = f"{
                        feedback.student.first_name
                    } {feedback.student.last_name}"
                    feedback_provided = feedback.feedback
                    feedback_date_utc = feedback.created_at
                    feedback_date_local = self.convert_to_localtime(feedback_date_utc)
                    feedback_list.append(
                        {
                            "student": feedback_provided_by_student_full_name,
                            "feedback": feedback_provided,
                            "date": feedback_date_local,
                        }
                    )

            # Course Material
            course_material_list = []
            materials = CourseMaterial.objects.filter(
                course__id=course_id
            )  # list of materials
            if len(materials) > 0:
                for material in materials:
                    upload = material.upload  # may be empty string ("")
                    id = material.id
                    title = material.title
                    content = material.content
                    duration = material.duration
                    if upload:
                        upload_name = upload.name.split("/")[-1]
                        course_material_list.append(
                            {
                                "id": id,
                                "hasFile": True,
                                "fileName": upload_name,
                                "title": title,
                                "content": content,
                                "duration": duration,
                            }
                        )
                    else:
                        course_material_list.append(
                            {
                                "id": id,
                                "hasFile": False,
                                "title": title,
                                "content": content,
                                "duration": duration,
                            }
                        )

            response = {
                "name": course_name,
                "category": course_category,
                "subcategory": course_subcategory,
                "description": course_description,
                "enrolled_student": enrolled_student_list,
                "author": f"{author_first_name} {author_last_name}",
                "author_username": author_username,
                "feedback_count": feedback_count,
                "feedback": feedback_list,
                "course_material": course_material_list,
            }

            return Response(
                response,
                status=status.HTTP_200_OK,
            )
        except Exception as e:
            return Response(
                e.args,
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )


class ListCourseByUserView(APIView):
    """
    Protected route - List courses that are either authored or enrolled by an authenticated user

    Params:
    @username: Username of the authenticated user
    """

    permission_classes = [IsAuthenticated]

    def validate_user(self, request_header, username) -> bool:
        access_token = request_header.get("Authorization").split(" ")[-1]
        jwt_secret = os.getenv("SECRET")
        decoded = jwt.decode(access_token, jwt_secret, algorithms="HS256")
        decoded_username = decoded.get("username")

        if username != decoded_username:
            raise ValidationError({"Error": "Bearer token does not match username"})
        else:
            return

    def get(self, request, username):
        header = request.headers

        # get user's role
        user_role = Role.objects.filter(userRole__username=username)[0].role

        try:
            self.validate_user(header, username)

            formatted_response = {"user": username, "courses": []}

            if user_role == "student":
                user_courses = CourseTracker.objects.filter(
                    Q(user__username=username) & Q(profile="learner")
                ).values("course", "is_blocked")

            elif user_role == "teacher":
                user_courses = CourseTracker.objects.filter(
                    Q(user__username=username) & Q(profile="author")
                ).values("course", "is_blocked")

            for course in user_courses:
                course_id = course.get("course")
                learner_is_blocked = course.get("is_blocked")
                _course = Course.objects.filter(id=course_id).values(
                    "category", "name", "subcategory"
                )
                enrolled_course_category = _course[0].get("category")
                enrolled_course_subcategory = _course[0].get("subcategory")
                enrolled_course_name = _course[0].get("name")

                if user_role == "student":
                    author = CourseTracker.objects.filter(
                        Q(course__id=course_id) & Q(profile="author")
                    )[0].user

                    author_full_name = f"{author.first_name} {author.last_name}"

                elif user_role == "teacher":
                    author = User.objects.get(username=username)
                    author_full_name = f"{author.first_name} {author.last_name}"

                formatted_response.get("courses").append(
                    {
                        "name": enrolled_course_name,
                        "category": enrolled_course_category,
                        "subcategory": enrolled_course_subcategory,
                        "author": author_full_name,
                        "id": course_id,
                        "is_blocked": learner_is_blocked,
                    }
                )

            # existing_status = Status.objects.filter(userStatus__username=username)[
            #     0
            # ].status
            # Status.objects.filter(userStatus__username=username).update(
            #     status=new_status
            # )

            # response = {
            #     "username": username,
            #     "existing_status": existing_status,
            #     "new_status": new_status,
            # }
            return Response(formatted_response, status=status.HTTP_200_OK)

        except ValidationError as e:
            return Response(e.args[0], status=status.HTTP_401_UNAUTHORIZED)

        except Exception as e:
            return Response(e.args, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class CreateUserCourseView(APIView):
    """
    Protected route - Create new course
    """

    permission_classes = [IsAuthenticated]

    def validate_user(self, request_header, username) -> bool:
        access_token = request_header.get("Authorization").split(" ")[-1]
        jwt_secret = os.getenv("SECRET")
        decoded = jwt.decode(access_token, jwt_secret, algorithms="HS256")
        decoded_username = decoded.get("username")
        decoded_role = decoded.get("role")

        if username != decoded_username:
            raise ValidationError({"Error": "Bearer token does not match username"})

        if decoded_role != "teacher":
            raise ValidationError(
                {"Error": "Only user who is a teacher can create new course"}
            )

        else:
            return

    def post(self, request, format=None):
        data = request.data
        username = data.get("author")
        header = request.headers

        try:
            self.validate_user(header, username)
            serializer = CreateCourseSerializer(data=data)
            if serializer.is_valid():
                author = serializer.validated_data.pop("author")  # username
                user_obj = User.objects.get(username=author)
                course_unique_id = uuid4()
                course_tracker_unique_id = uuid4()
                with transaction.atomic():
                    created_course = Course.objects.create(
                        id=course_unique_id, **serializer.validated_data
                    )
                    created_course_id = created_course.id
                    CourseTracker.objects.create(
                        id=course_tracker_unique_id,
                        user=user_obj,
                        course=created_course,
                        profile="author",
                    )
            return Response({"id": created_course_id}, status=status.HTTP_201_CREATED)

        except ValidationError as e:
            return Response(e.args[0], status=status.HTTP_401_UNAUTHORIZED)

        except Exception as e:
            return Response(e.args, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class UpdateCourseUserBlockStatusView(APIView):
    """
    Protected route - Block or unblock student from a specific course

    Params:
    @username: Username of the authenticated user
    """

    permission_classes = [IsAuthenticated]

    def validate_user(self, request_header, username) -> bool:
        access_token = request_header.get("Authorization").split(" ")[-1]
        jwt_secret = os.getenv("SECRET")
        decoded = jwt.decode(access_token, jwt_secret, algorithms="HS256")
        decoded_username = decoded.get("username")

        if username != decoded_username:
            raise ValidationError({"Error": "Bearer token does not match username"})
        else:
            return

    def patch(self, request, course_id, student_id):
        data = request.data
        new_blocked_status = data.get("isBlocked")
        username = data.get("username")
        header = request.headers

        try:
            self.validate_user(header, username)

            serializer = UpdateCourseUserBlockStatusSerializer(data=data)
            if serializer.is_valid():
                # get user's role
                CourseTracker.objects.filter(
                    Q(course__id=course_id)
                    & Q(profile="learner")
                    & Q(user__id=student_id)
                ).update(is_blocked=new_blocked_status)

            response = {
                "id": student_id,
                "username": username,
                "isBlocked": new_blocked_status,
            }

            return Response(response, status=status.HTTP_200_OK)

        except ValidationError as e:
            return Response(e.args[0], status=status.HTTP_401_UNAUTHORIZED)

        except Exception as e:
            return Response(e.args, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class EnrollUserCourseView(APIView):

    permission_classes = [IsAuthenticated]

    def validate_user(self, request_header, username) -> bool:
        access_token = request_header.get("Authorization").split(" ")[-1]
        jwt_secret = os.getenv("SECRET")
        decoded = jwt.decode(access_token, jwt_secret, algorithms="HS256")
        decoded_username = decoded.get("username")

        if username != decoded_username:
            raise ValidationError({"Error": "Bearer token does not match username"})
        else:
            return

    def post(self, request, format=None):
        data = request.data
        header = request.headers

        try:
            course_id = data.get("courseId")
            student_username = data.get("studentUsername")
            self.validate_user(header, student_username)

            course_to_enroll = Course.objects.get(id=course_id)
            student_obj = User.objects.get(username=student_username)
            unique_coursetracker_id = uuid4()
            CourseTracker.objects.create(
                id=unique_coursetracker_id,
                user=student_obj,
                course=course_to_enroll,
                is_blocked=False,
                profile="learner",
            )

            return Response("OK", status=status.HTTP_200_OK)

        except Exception as e:
            return Response(e.args, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class AddCourseReviewView(APIView):

    permission_classes = [IsAuthenticated]

    def validate_user(self, request_header, username) -> bool:
        access_token = request_header.get("Authorization").split(" ")[-1]
        jwt_secret = os.getenv("SECRET")
        decoded = jwt.decode(access_token, jwt_secret, algorithms="HS256")
        decoded_username = decoded.get("username")

        if username != decoded_username:
            raise ValidationError({"Error": "Bearer token does not match username"})
        else:
            return

    def post(self, request, course_id):
        data = request.data
        header = request.headers

        try:
            username = data.get("username")
            review = data.get("review")
            self.validate_user(header, username)

            serializer = AddCourseReviewSerializer(data=data)

            if serializer.is_valid():
                course_to_add_review = Course.objects.get(id=course_id)
                student_obj = User.objects.get(username=username)

                unique_studenfeedback_id = uuid4()
                StudentFeedback.objects.create(
                    id=unique_studenfeedback_id,
                    student=student_obj,
                    course=course_to_add_review,
                    feedback=review,
                )

                return Response("OK", status=status.HTTP_200_OK)

            else:
                return Response(serializer.errors, status=status.HTTP_401_UNAUTHORIZED)

        except Exception as e:
            return Response(e.args, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class RemoveStudentFromCourseView(APIView):

    permission_classes = [IsAuthenticated]

    def validate_user(self, request_header, username) -> bool:
        access_token = request_header.get("Authorization").split(" ")[-1]
        jwt_secret = os.getenv("SECRET")
        decoded = jwt.decode(access_token, jwt_secret, algorithms="HS256")
        decoded_username = decoded.get("username")

        if username != decoded_username:
            raise ValidationError({"Error": "Bearer token does not match username"})
        else:
            return

    def delete(self, request, course_id):
        data = request.data
        header = request.headers

        try:
            student_username_to_delete = data.get("studentUsername")
            username = data.get("authenticatedUsername")

            self.validate_user(header, username)

            serializer = RemoveStudentFromCourseSerializer(data=data)

            if serializer.is_valid():
                with transaction.atomic():

                    # remove student from course
                    CourseTracker.objects.filter(
                        Q(user__username=student_username_to_delete)
                        & Q(profile="learner")
                        & Q(course__id=course_id)
                    ).delete()
                return Response("OK", status=status.HTTP_204_NO_CONTENT)

            else:
                return Response(serializer.errors, status=status.HTTP_401_UNAUTHORIZED)

        except Exception as e:
            return Response(e.args, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
