"""
Setup global urls
- admin/ -> Admin urls
- api/user/register/ -> Create new user
- api/token/ -> Get access token
- api/token/refresh/ -> Get refresh token
- api/ -> api endpoints

"""

from django.contrib import admin
from django.urls import path, include

from api.views.views_user import CreateUserView
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from api.views.views_custom_token import MyTokenObtainPairView

urlpatterns = [
    path("admin/", admin.site.urls),
    path("api/user/register/", CreateUserView.as_view(), name="register"),
    path("api/token/", MyTokenObtainPairView.as_view(), name="get_token"),
    path("api/token/refresh/", TokenRefreshView.as_view(), name="refresh"),
    # path("api-auth/", include("rest_framework.urls")),
    path("api/", include("api.urls")),
]
