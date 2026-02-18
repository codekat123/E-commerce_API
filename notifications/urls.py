from django.urls import path
from .views import (
    CreateNotificationView,
    ListNotificationView,
    NotificationRetrieveView,
    NotificationUpdateView
)


app_name = 'notifications'


urlpatterns = [
    path('create/', CreateNotificationView.as_view(), name='create-notification'),
    path('list/', ListNotificationView.as_view(), name='list-notifications'),
    path('<int:id>/', NotificationRetrieveView.as_view(), name='retrieve-notification'),
    path('<int:id>/update/', NotificationUpdateView.as_view(), name='update-notification'),
]