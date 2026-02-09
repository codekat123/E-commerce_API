from .logout import LogoutAPIView
from .admin import StaffCreateAPIView , staff_set_password_view
from .login import LoginAPIView
from .normal_user import (
    RegisterAPIView,
    ActivateUser,
    ProfileUpdateAPIView,
    ProfileRetrieveAPIView,
    SelfDeleteAPIView
    )