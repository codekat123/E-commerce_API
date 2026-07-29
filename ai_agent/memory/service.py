from django.conf import settings
from langchain_core.messages import (
    AIMessage,
    BaseMessage,
    HumanMessage,
    SystemMessage,
    ToolMessage,
)

from ai_agent.models import Conversation, Message, MessageRole

_MESSAGE_CLASS_MAP: dict[
    MessageRole,
    type[BaseMessage],
] = {
    MessageRole.USER: HumanMessage,
    MessageRole.ASSISTANT: AIMessage,
    MessageRole.SYSTEM: SystemMessage,
}


class MemoryService:
    """
    Loads conversation history and converts it into LangChain messages.
    """

    def __init__(self) -> None:
        self._history_limit = settings.AI_AGENT["MEMORY_HISTORY_LIMIT"]

    def get_context_messages(
        self,
        conversation: Conversation,
    ) -> list[BaseMessage]:
        messages = self._load_messages(
            conversation=conversation,
        )

        return self._convert_to_langchain_messages(
            messages=messages,
        )

    def _load_messages(
        self,
        conversation: Conversation,
    ) -> list[Message]:
        messages = list(
            Message.objects.filter(
                conversation=conversation,
            )
            .only(
                "role",
                "content",
                "created_at",
                "tool_calls",
                "tool_call_id",
                "tool_name",
            )
            .order_by("-created_at")[: self._history_limit]
        )

        messages.reverse()

        return messages

    def _convert_to_langchain_messages(
        self,
        messages: list[Message],
    ) -> list[BaseMessage]:
        context_messages: list[BaseMessage] = []

        for message in messages:
            if message.role == MessageRole.TOOL:
                context_messages.append(
                    ToolMessage(
                        content=message.content,
                        tool_call_id=message.tool_call_id,
                        name=message.tool_name,
                    )
                )
                continue

            if message.role == MessageRole.ASSISTANT:
                context_messages.append(
                    AIMessage(
                        content=message.content,
                        tool_calls=message.tool_calls,
                    )
                )
                continue

            message_class = _MESSAGE_CLASS_MAP.get(message.role)

            if message_class is None:
                raise ValueError(f"Unsupported message role: {message.role}")

            context_messages.append(
                message_class(
                    content=message.content,
                )
            )

        return context_messages
