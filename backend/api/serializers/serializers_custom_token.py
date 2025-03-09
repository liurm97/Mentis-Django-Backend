from rest_framework_simplejwt.serializers import TokenObtainSerializer, RefreshToken

from ..models import Role


class MyTokenObtainPairSerializer(TokenObtainSerializer):
    token_class = RefreshToken

    def validate(self, attrs):
        # validate username, password
        data = super().validate(attrs)

        # create refresh token
        refresh = self.get_token(self.user)

        role = (
            Role.objects.filter(userRole__username=self.user)
            .values("role")[0]
            .get("role")
        )

        username = self.user.username
        firstname = self.user.first_name
        lastname = self.user.last_name
        refresh["role"] = role
        refresh["username"] = username
        refresh["firstname"] = firstname
        refresh["lastname"] = lastname

        data["refresh"] = str(refresh)
        data["access"] = str(refresh.access_token)

        return data
