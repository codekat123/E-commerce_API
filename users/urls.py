from django.urls import path
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)
from .views import (
    RegisterAPIView,
    ActivateUser,
    LogoutAPIView,
    StaffCreateAPIView,
    staff_set_password_view,
)

app_name = "users"

urlpatterns = [
    # Auth
    path("auth/login/", TokenObtainPairView.as_view(), name="login"),
    path("auth/token/refresh/", TokenRefreshView.as_view(), name="token_refresh"),
    path("auth/logout/", LogoutAPIView.as_view(), name="logout"),

    # Registration & activation
    path("auth/register/", RegisterAPIView.as_view(), name="register"),
    path(
        "auth/activate/<uuid:uuid>/<str:token>/",
        ActivateUser.as_view(),
        name="activate",
    ),

    # Staff
    path("staff/", StaffCreateAPIView.as_view(), name="staff_create"),
    path(
        "staff/set-password/<uuid:uuid>/<str:token>/",
        staff_set_password_view,
        name="staff_set_password",
    ),
]
