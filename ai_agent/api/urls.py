from django.urls import path

from ai_agent.api.views import ChatAPIView

app_name = "ai_agent"

urlpatterns = [
    path(
        "chat/",
        ChatAPIView.as_view(),
        name="ai-chat",
    ),
]
