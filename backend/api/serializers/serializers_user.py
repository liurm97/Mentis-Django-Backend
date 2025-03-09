from django.contrib.auth.models import User
from rest_framework import serializers
from ..models import Role, Interest, Status
from uuid import uuid4
from django.db import transaction


class InterestSerializer(serializers.Serializer):
    interest = serializers.CharField()

    class Meta:
        fields = "interest"


class CustomUserSerializer(serializers.Serializer):
    """
    Custom serializer for User and Role tables during user signup
    """

    username = serializers.CharField()
    first_name = serializers.CharField()
    last_name = serializers.CharField()
    email = serializers.CharField()
    role = serializers.CharField()
    password = serializers.CharField(write_only=True)
    interest = InterestSerializer(many=True, required=False)

    class Meta:
        fields = [
            "username",
            "password",
            "first_name",
            "last_name",
            "email",
            "interest",
        ]

    def validate_email(self, data):
        """
        Validate email is unique. Else raise ValidationError
        """

        # get all emails
        emails = list(User.objects.values_list("email", flat=True))

        # validate email is unique, else raise ValidationError
        if data in emails:

            raise serializers.ValidationError("Email must be unique")

        else:
            return data

    def create(self, validated_data):
        """
        If data is valid, create user and insert into Role table
        """
        interest_key_exists = False
        role = validated_data.pop("role")
        if "interest" in validated_data:
            interest_key_exists = True
            interests = validated_data.pop("interest")

        try:
            with transaction.atomic():

                # Insert into User table
                created_user = User.objects.create_user(**validated_data)

                # Insert into Role table
                Role.objects.create(role=role, userRole=created_user)

                # Insert into Interest table (only applies to student user)
                if interest_key_exists == True:
                    interest_payload = []
                    for interest in interests:
                        interest_unique_id = uuid4()
                        interest_payload.append(
                            Interest(
                                id=interest_unique_id,
                                interest=interest["interest"],
                                studentInterest=created_user,
                            )
                        )
                    Interest.objects.bulk_create(interest_payload)

                # Insert into Status table
                status_unique_id = uuid4()
                Status.objects.create(id=status_unique_id, userStatus=created_user)

        except Exception as e:
            raise serializers.ValidationError(e.args)

        return created_user
