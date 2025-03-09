from django.contrib.auth.models import User
from rest_framework import serializers
from ..models import Course, CourseMaterial
from uuid import uuid4


class AddCourseMaterialSerializer(serializers.Serializer):
    title = serializers.CharField()
    content = serializers.CharField()
    upload = serializers.FileField(required=False)
    duration = serializers.IntegerField()

    class Meta:
        fields = ("title", "content", "upload", "duration")
