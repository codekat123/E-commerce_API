from django.urls import path
from rest_framework_simplejwt.views import TokenObtainPairView,TokenRefreshView
from .views import (
    RegisterAPIView,
    ActivateUser,
    LogoutAPIView
)
app_name = 'users'

urlpatterns = [
    path('login/',TokenObtainPairView.as_view(),name='login'),
    path('login/refresh/',TokenRefreshView.as_view(),name='refresh_token'),
    path('register/',RegisterAPIView.as_view(),name='register'),
    path('activate/<str:token>/<uuid>/',ActivateUser.as_view(),name='activation_user'),
    path('logout/',LogoutAPIView.as_view(),name='logout'),

]