from __future__ import annotations

from unittest.mock import MagicMock, PropertyMock, patch

from django.contrib.auth import get_user_model
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from rest_framework_simplejwt.tokens import RefreshToken

from ai_agent.api.views import ChatAPIView
from ai_agent.models.conversation import Conversation
from ai_agent.service.dto import ChatResult

User = get_user_model()


class ChatAPIViewTests(APITestCase):
    def setUp(self) -> None:
        self.user = User.objects.create_user(
            email="john@example.com",
            password="password123",
            is_active=True,
        )

        refresh = RefreshToken.for_user(self.user)

        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {refresh.access_token}")

        self.url = reverse("ai_agent:ai-chat")

    def test_requires_authentication(self) -> None:
        self.client.credentials()

        response = self.client.post(
            self.url,
            {"message": "Hello"},
            format="json",
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_401_UNAUTHORIZED,
        )

    @patch.object(
        ChatAPIView,
        "chat_service",
        new_callable=PropertyMock,
    )
    def test_chat_returns_response(
        self,
        mock_chat_service,
    ) -> None:
        conversation = Conversation.objects.create(
            user=self.user,
        )

        service = MagicMock()

        service.chat.return_value = ChatResult(
            conversation=conversation,
            response="Hello from AI!",
        )

        mock_chat_service.return_value = service

        response = self.client.post(
            self.url,
            {
                "message": "Hello",
            },
            format="json",
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK,
        )

        self.assertEqual(
            response.data["conversation_id"],
            str(conversation.id),
        )

        self.assertEqual(
            response.data["response"],
            "Hello from AI!",
        )

        service.chat.assert_called_once()

    def test_invalid_request_returns_400(self) -> None:
        response = self.client.post(
            self.url,
            {},
            format="json",
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_400_BAD_REQUEST,
        )
