from django.conf import settings
import mimetypes
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
from django.conf import settings

from django.http import FileResponse, HttpResponse
from wsgiref.util import FileWrapper
from ..serializers.serializers_course_material import AddCourseMaterialSerializer
from django.db.utils import IntegrityError
from rest_framework import serializers
from api.models import Course, CourseTracker, StudentFeedback, CourseMaterial, Role
from django.db.models import Q
from datetime import datetime
import pytz
from django.utils import timezone
from django.db import transaction

class AddCourseMaterialView(APIView):
    """
    Protected route - Add course material to course
    """

    permission_classes = [IsAuthenticated]

    def validate_user(self, request_header, username) -> bool:
        access_token = request_header.get("Authorization").split(" ")[-1]
        jwt_secret = settings.SECRET_KEY
        decoded = jwt.decode(access_token, jwt_secret, algorithms="HS256")
        decoded_username = decoded.get("username")

        if username != decoded_username:
            raise ValidationError({"Error": "Bearer token does not match username"})
        else:
            return

    def post(self, request, course_id):
        data = request.data
        header = request.headers
        serializer = AddCourseMaterialSerializer(data=data)

        username = data.get("authenticatedUsername")
        try:
            self.validate_user(header, username)
            if serializer.is_valid():
                course = Course.objects.get(id=course_id)
                unique_coursematerial_id = uuid4()

                # If upload is provided
                if "upload" in data.keys():
                    CourseMaterial.objects.create(
                        id=unique_coursematerial_id,
                        content=data.get("content"),
                        upload=data.get("upload"),
                        title=data.get("title"),
                        duration=data.get("duration"),
                        course=course,
                    )
                else:
                    # If upload is not provided provided
                    CourseMaterial.objects.create(
                        id=unique_coursematerial_id,
                        content=data.get("content"),
                        title=data.get("title"),
                        duration=data.get("duration"),
                        course=course,
                    )
                return Response(
                    "OK",
                    status=status.HTTP_201_CREATED,
                )
            return Response(
                "OK",
                status=status.HTTP_400_BAD_REQUEST,
            )

        except Exception as e:
            return Response(
                e.args,
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )


class DownloadCourseMaterialAttachmentView(APIView):
    """
    Protected route - Download course material attachment
    """

    permission_classes = [IsAuthenticated]

    def validate_user(self, request_header, username) -> bool:
        access_token = request_header.get("Authorization").split(" ")[-1]
        jwt_secret = settings.SECRET_KEY
        decoded = jwt.decode(access_token, jwt_secret, algorithms="HS256")
        decoded_username = decoded.get("username")

        if username != decoded_username:
            raise ValidationError({"Error": "Bearer token does not match username"})
        else:
            return

    def post(self, request):
        data = request.data
        header = request.headers

        username = data.get("authenticatedUsername")
        material_id = data.get("materialId")

        try:
            self.validate_user(header, username)

            material = CourseMaterial.objects.get(id=material_id)

            full_path = os.path.join(settings.MEDIA_ROOT, material.upload.path)

            material_file_handle = full_path

            document = open(material_file_handle, "rb")

            content = document.read()

            response = HttpResponse(
                content,
                content_type=mimetypes.guess_type(full_path),
            )
            return response

        except Exception as e:
            return Response(
                e.args,
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )
