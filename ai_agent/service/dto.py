from __future__ import annotations

from dataclasses import dataclass

from ai_agent.models.conversation import Conversation


@dataclass(frozen=True, slots=True)
class ChatResult:
    """
    Result returned by ChatService after completing a chat request.
    """

    conversation: Conversation
    response: str
