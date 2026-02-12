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

    # Authentication
    path("auth/login/", LoginAPIView.as_view(), name="login"),
    path("auth/refresh/", TokenRefreshView.as_view(), name="token_refresh"),
    path("auth/logout/", LogoutAPIView.as_view(), name="logout"),

    # Registration
    path("auth/register/", RegisterAPIView.as_view(), name="register"),
    path(
        "auth/activate/<uuid:uuid>/<str:token>/",
        ActivateUser.as_view(),
        name="activate",
    ),

    # Profile (self)
    path("profile/", ProfileRetrieveAPIView.as_view(), name="profile_detail"),     # GET
    path("profile/update/", ProfileUpdateAPIView.as_view(), name="profile_update"), # PUT/PATCH
    path("profile/delete/", SelfDeleteAPIView.as_view(), name="profile_delete"),   # DELETE

    # Staff management
    path("staff/", StaffCreateAPIView.as_view(), name="staff_create"),
    path(
        "staff/set-password/<uuid:uuid>/<str:token>/",
        staff_set_password_view,
        name="staff_set_password",
    ),
]
