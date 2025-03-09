import os
from django.contrib.auth.models import User
from rest_framework import generics
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.exceptions import ValidationError
from ..serializers.serializers_status import (
    PatchUserStatusSerializer,
    GetUserStatusSerializer,
)
from django.db.utils import IntegrityError
from rest_framework import serializers
from api.models import Status
from django.db.models import Q
from datetime import datetime
import pytz
from django.utils import timezone
import jwt
from django.core.exceptions import ValidationError


class UserStatus(APIView):

    # Allow any access
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

    def patch(self, request, format=None):
        data = request.data
        header = request.headers

        new_status = data.get("status")
        username = data.get("username")

        try:
            self.validate_user(header, username)
            serializer = PatchUserStatusSerializer(data=data)

            if serializer.is_valid():
                existing_status = Status.objects.filter(userStatus__username=username)[
                    0
                ].status
                Status.objects.filter(userStatus__username=username).update(
                    status=new_status
                )

                response = {
                    "username": username,
                    "existing_status": existing_status,
                    "new_status": new_status,
                }
                return Response(response, status=status.HTTP_200_OK)
            else:
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        except ValidationError as e:
            return Response(e.args[0], status=status.HTTP_401_UNAUTHORIZED)

        except Exception as e:
            return Response(e.args, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def post(self, request, format=None):
        data = request.data
        header = request.headers

        username = data.get("username")
        try:
            self.validate_user(header, username)
            serializer = GetUserStatusSerializer(data=data)
            if serializer.is_valid():

                existing_status = Status.objects.filter(userStatus__username=username)[
                    0
                ].status
                return Response({"status": existing_status}, status=status.HTTP_200_OK)
            else:
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        except ValidationError as e:
            return Response(e.args[0], status=status.HTTP_401_UNAUTHORIZED)

        except Exception as e:
            return Response(e.args, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
