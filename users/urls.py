from django.urls import path
from rest_framework_simplejwt.views import TokenRefreshView

from .views import (
    RegisterAPIView,
    ActivateUser,
    LogoutAPIView,
    StaffCreateAPIView,
    staff_set_password_view,
    ProfileUpdateAPIView,
    ProfileRetrieveAPIView,
    SelfDeleteAPIView,
    LoginAPIView,
)

app_name = "users"

urlpatterns = [

    path("auth/login/", LoginAPIView.as_view(), name="login"),
    path("auth/refresh/", TokenRefreshView.as_view(), name="token_refresh"),
    path("auth/logout/", LogoutAPIView.as_view(), name="logout"),


    path("auth/register/", RegisterAPIView.as_view(), name="register"),
    path(
        "auth/activate/<uuid:uuid>/<str:token>/",
        ActivateUser.as_view(),
        name="activate",
    ),


    path("profile/", ProfileRetrieveAPIView.as_view(), name="get_profile"),
    path("profile/update/", ProfileUpdateAPIView.as_view(), name="update_profile"),
    path("profile/delete/", SelfDeleteAPIView.as_view(), name="self_delete"),


    path("staff/", StaffCreateAPIView.as_view(), name="staff_create"),
    path(
        "staff/set-password/<uuid:uuid>/<str:token>/",
        staff_set_password_view,
        name="staff_set_password",
    ),
]
