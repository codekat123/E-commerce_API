from __future__ import annotations

from uuid import UUID

from django.contrib.auth import get_user_model

from ai_agent.models.conversation import Conversation
from ai_agent.models.message import Message, MessageRole

User = get_user_model()


class ConversationService:
    """Handles conversation and message persistence."""

    def create_conversation(
        self,
        *,
        user: User,
    ) -> Conversation:
        return Conversation.objects.create(user=user)

    def get_conversation(
        self,
        *,
        user: User,
        conversation_id: UUID,
    ) -> Conversation:
        return Conversation.objects.get(
            id=conversation_id,
            user=user,
        )

    def add_user_message(
        self,
        *,
        conversation: Conversation,
        content: str,
    ) -> Message:
        return self._create_message(
            conversation=conversation,
            role=MessageRole.USER,
            content=content,
        )

    def add_assistant_message(
        self,
        *,
        conversation: Conversation,
        content: str,
    ) -> Message:
        return self._create_message(
            conversation=conversation,
            role=MessageRole.ASSISTANT,
            content=content,
        )

    def _create_message(
        self,
        *,
        conversation: Conversation,
        role: MessageRole,
        content: str,
    ) -> Message:
        return Message.objects.create(
            conversation=conversation,
            role=role,
            content=content,
        )
