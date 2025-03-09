from django.utils import timezone
import os
from django.shortcuts import render
from django.contrib.auth.models import User
from django.db.models import Q
import jwt
import pytz
from rest_framework import generics
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.exceptions import ValidationError

from ..models import Role, Interest, CourseTracker, Course, Status
from ..serializers.serializers_user import CustomUserSerializer
from django.db.utils import IntegrityError
from rest_framework import serializers
from django.conf import settings


class CreateUserView(APIView):
    """
    View to register new user
    - Insert into `User` table
    - Insert into `Role` table
    - Insert into `Status` table with default status = `active`
    """

    # Allow any access
    permission_classes = [AllowAny]

    def post(self, request, format=None):
        serializer = CustomUserSerializer(data=request.data)
        try:
            if serializer.is_valid():
                serializer.save()

                serializer.validated_data.pop("password")
                return Response(
                    serializer.validated_data,
                    status=status.HTTP_201_CREATED,
                )

            else:
                return Response(
                    f"The provided email ({request.data['email']}) is not unique. Please try again.",
                    status=status.HTTP_400_BAD_REQUEST,
                )

        except IntegrityError:
            return Response(
                f"The provided username ({request.data['username']}) is not unique. Please try again.",
                status=status.HTTP_400_BAD_REQUEST,
            )

        except serializers.ValidationError as e:
            return Response(
                e.detail,
                status=status.HTTP_400_BAD_REQUEST,
            )


class ListUsersView(APIView):
    """
    View to list all users
    """

    permission_classes = [IsAuthenticated]

    def validate_user(self, request_header, username) -> bool:
        access_token = request_header.get("Authorization").split(" ")[-1]
        # jwt_secret = os.getenv("SECRET_KEY")
        jwt_secret = settings.SECRET_KEY
        decoded = jwt.decode(access_token, jwt_secret, algorithms="HS256")
        decoded_username = decoded.get("username")

        if username != decoded_username:
            raise ValidationError({"Error": "Bearer token does not match username"})
        else:
            return

    def post(self, request):
        data = request.data
        username = data.get("username")
        header = request.headers

        try:
            self.validate_user(header, username)
            users = User.objects.all().values_list(
                "username", "first_name", "last_name"
            )
            user_list = []
            for user in users:
                username, first_name, last_name = user
                print(username)
                if username != "admin":
                    full_name = f"{first_name} {last_name}"
                    role = Role.objects.filter(userRole__username=username)[0].role
                    user_list.append(
                        {"fullname": full_name, "role": role, "username": username}
                    )
                    sorted_user_list = sorted(user_list, key=lambda x: x["fullname"])
            print(sorted_user_list)
            return Response(sorted_user_list, status=status.HTTP_200_OK)

        except ValidationError as e:
            return Response(e.args[0], status=status.HTTP_401_UNAUTHORIZED)

        except Exception as e:
            return Response(e.args, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class ListUserDetailView(APIView):
    """
    View to details of a single user
        - First name
        - Last name
        - Interests
        - Recently enrolled courses (up to 4)
    """

    permission_classes = [AllowAny]

    def convert_to_localtime(self, utctime):
        fmt = "%b %d, %Y"
        utc = utctime.replace(tzinfo=pytz.UTC)
        localtz = utc.astimezone(timezone.get_current_timezone())
        return localtz.strftime(fmt)

    def get(self, request, username):
        try:

            # Get user name
            user = User.objects.get(username=username)
            first_name = user.first_name
            last_name = user.last_name

            # Get user role
            role = Role.objects.get(userRole__username=username).role

            # Get user interests
            interests = list(
                Interest.objects.filter(studentInterest__username=username).values(
                    "interest"
                )
            )

            if role == "student":
                # Get user's recently enrolled courses (up to 4)
                courses = CourseTracker.objects.filter(
                    Q(user__username=username) & Q(profile="learner")
                ).values("course", "created_at")[:4]

            elif role == "teacher":
                # Get user's recently authored courses (up to 4)
                courses = CourseTracker.objects.filter(
                    Q(user__username=username) & Q(profile="author")
                ).values("course", "created_at")[:4]

            sorted_courses = sorted(courses, key=lambda x: x["created_at"])

            courses_details = []

            userStatus = Status.objects.get(userStatus__username=username).status

            for course in sorted_courses:
                id = course.get("course")

                name = Course.objects.get(id=id).name

                enrolled_date_utc = course.get("created_at")
                enrolled_date_local = self.convert_to_localtime(enrolled_date_utc)

                subcategory = Course.objects.get(id=id).subcategory
                category = Course.objects.get(id=id).category

                author = CourseTracker.objects.get(
                    Q(course__id=id) & Q(profile="author")
                ).user

                author_full_name = f"{author.first_name} {author.last_name}"

                course_detail = {
                    "id": id,
                    "name": name,
                    "subcategory": subcategory,
                    "category": category,
                    "author": author_full_name,
                    "enrolled_date": enrolled_date_local,
                }

                courses_details.append(course_detail)

            response = {
                "firstname": first_name,
                "lastname": last_name,
                "status": userStatus,
                "role": role,
                "interests": interests,
                "courses": courses_details,
            }

            return Response(response, status=status.HTTP_200_OK)

        except ValidationError as e:
            return Response(e.args[0], status=status.HTTP_401_UNAUTHORIZED)

        except Exception as e:
            return Response(e.args, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
