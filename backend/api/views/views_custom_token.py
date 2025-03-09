from rest_framework_simplejwt.views import TokenViewBase
from ..serializers.serializers_custom_token import MyTokenObtainPairSerializer


class MyTokenObtainPairView(TokenViewBase):
    serializer_class = MyTokenObtainPairSerializer
