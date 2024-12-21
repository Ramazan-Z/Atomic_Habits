from django.urls import path
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

from users import views
from users.apps import UsersConfig

app_name = UsersConfig.name

urlpatterns = [
    path("register/", views.UserRegisterView.as_view(), name="register"),
    path("login/", TokenObtainPairView.as_view(), name="login"),
    path("refresh_token/", TokenRefreshView.as_view(), name="refresh-token"),
    path("profile/", views.UserProfileView.as_view(), name="profile"),
    path("update/", views.UserUpdateView.as_view(), name="update"),
]
