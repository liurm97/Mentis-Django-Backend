from django.contrib.auth.models import User
from rest_framework import serializers
from ..models import Course
from uuid import uuid4


class PatchUserStatusSerializer(serializers.Serializer):
    """
    Serializer for PATCH /user/status endpoint
    """

    username = serializers.CharField()
    status = serializers.CharField()

    class Meta:
        fields = ("username", "status")


class GetUserStatusSerializer(serializers.Serializer):
    """
    Serializer for GET /user/status endpoint
    """

    username = serializers.CharField()

    class Meta:
        fields = "username"
