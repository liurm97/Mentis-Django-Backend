from django.contrib.auth.models import User
from rest_framework import serializers
from ..models import Course
from uuid import uuid4


class ListCoursesSerializer(serializers.Serializer):
    category = serializers.CharField()
    limit = serializers.IntegerField(required=False)

    class Meta:
        fields = ("category", "limit")

    def validate_category(self, data):
        if data not in ["business", "development", "personal_development"]:
            raise serializers.ValidationError(
                f"You have provided ({data}). category must be one of ['business', 'development', 'personal_development']"
            )
        return data

    def validate_limit(self, data):
        if data <= 0:
            raise serializers.ValidationError(
                f"You have provided ({data}). limit value must be a positive integer."
            )
        return data


class CreateCourseSerializer(serializers.Serializer):
    name = serializers.CharField()
    category = serializers.CharField()
    subcategory = serializers.CharField()
    description = serializers.CharField()
    author = serializers.CharField()

    class Meta:
        fields = ("name", "category", "subcategory", "description", "author")

    def validate_category(self, data):
        if data not in ["business", "development", "personal_development"]:
            raise serializers.ValidationError(
                f"You have provided ({data}). category must be one of ['business', 'development', 'personal_development']"
            )
        return data


class UpdateCourseUserBlockStatusSerializer(serializers.Serializer):
    username = serializers.CharField()
    isBlocked = serializers.BooleanField()

    class Meta:
        fields = ("username", "isBlocked")


class AddCourseReviewSerializer(serializers.Serializer):
    username = serializers.CharField()
    review = serializers.CharField()

    def validate_review(self, data):
        if len(data) == 0:
            raise serializers.ValidationError(f"Review cannot be empty")
        return data

    class Meta:
        fields = ("username", "review")


class RemoveStudentFromCourseSerializer(serializers.Serializer):
    authenticatedUsername = serializers.CharField()
    studentUsername = serializers.CharField()

    class Meta:
        fields = ("authenticatedUsername", "studentUsername")
