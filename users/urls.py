from django.urls import path
from rest_framework_simplejwt.views import TokenObtainPairView,TokenRefreshView
from .views import RegisterAPIView
app_name = 'users'

urlpatterns = [
    path('login/',TokenObtainPairView.as_view(),name='login'),
    path('login/refresh/',TokenRefreshView.as_view(),name='refresh_token'),
    path('register/',RegisterAPIView.as_view(),name='register'),
]