from __future__ import annotations

from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from ai_agent.api.serializer import (
    ChatRequestSerializer,
    ChatResponseSerializer,
)
from ai_agent.service.chat_service import ChatService


class ChatAPIView(APIView):
    permission_classes = [IsAuthenticated]

    @property
    def chat_service(self) -> ChatService:
        return ChatService()

    def post(self, request):
        request_serializer = ChatRequestSerializer(
            data=request.data,
        )
        request_serializer.is_valid(raise_exception=True)

        result = self.chat_service.chat(
            user=request.user,
            message=request_serializer.validated_data["message"],
            conversation_id=request_serializer.validated_data.get("conversation_id"),
        )

        response_serializer = ChatResponseSerializer(
            data={
                "conversation_id": result.conversation.id,
                "response": result.response,
            }
        )
        response_serializer.is_valid(raise_exception=True)

        return Response(
            response_serializer.data,
            status=status.HTTP_200_OK,
        )
