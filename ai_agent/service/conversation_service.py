from __future__ import annotations

from uuid import UUID

from django.contrib.auth import get_user_model
from langchain_core.messages import (
    AIMessage,
    BaseMessage,
    HumanMessage,
    SystemMessage,
    ToolMessage,
)

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

    def add_langchain_message(
        self,
        *,
        conversation: Conversation,
        message: BaseMessage,
    ) -> Message:
        role = self._get_message_role(message)

        return self._create_message(
            conversation=conversation,
            role=role,
            content=message.content,
            tool_calls=getattr(message, "tool_calls", []),
            tool_call_id=getattr(
                message,
                "tool_call_id",
                None,
            ),
            tool_name=getattr(
                message,
                "name",
                None,
            ),
        )

    def _get_message_role(
        self,
        message: BaseMessage,
    ) -> MessageRole:
        if isinstance(message, HumanMessage):
            return MessageRole.USER

        if isinstance(message, AIMessage):
            return MessageRole.ASSISTANT

        if isinstance(message, ToolMessage):
            return MessageRole.TOOL

        if isinstance(message, SystemMessage):
            return MessageRole.SYSTEM

        raise ValueError(f"Unsupported message type: {type(message)}")

    def _create_message(
        self,
        *,
        conversation: Conversation,
        role: MessageRole,
        content: str,
        tool_calls: list | None = None,
        tool_call_id: str | None = None,
        tool_name: str | None = None,
    ) -> Message:
        return Message.objects.create(
            conversation=conversation,
            role=role,
            content=content,
            tool_calls=tool_calls or [],
            tool_call_id=tool_call_id,
            tool_name=tool_name,
        )
