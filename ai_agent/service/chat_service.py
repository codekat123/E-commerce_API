from __future__ import annotations

from uuid import UUID

from django.contrib.auth import get_user_model
from langchain_core.messages import AIMessage
from langgraph.graph.state import CompiledStateGraph

from ai_agent.graph.builder import get_graph
from ai_agent.graph.factory import GraphStateFactory
from ai_agent.graph.state import GraphState
from ai_agent.models.conversation import Conversation
from ai_agent.service.conversation_service import ConversationService
from ai_agent.service.dto import ChatResult

User = get_user_model()


class ChatService:
    """
    Orchestrates the AI chat workflow.

    Responsibilities:

    - Create or load conversations.
    - Persist user messages.
    - Execute the AI graph.
    - Persist assistant messages.
    - Return the chat result.
    """

    def __init__(
        self,
        *,
        graph: CompiledStateGraph | None = None,
        conversation_service: ConversationService | None = None,
    ) -> None:
        self._graph: CompiledStateGraph = graph or get_graph()

        self._conversation_service: ConversationService = (
            conversation_service or ConversationService()
        )

    def chat(
        self,
        *,
        user: User,
        message: str,
        conversation_id: UUID | None = None,
    ) -> ChatResult:

        conversation = self._get_or_create_conversation(
            user=user,
            conversation_id=conversation_id,
        )

        self._conversation_service.add_user_message(
            conversation=conversation,
            content=message,
        )

        initial_state = self._build_initial_state(
            message=message,
        )

        final_state = self._graph.invoke(initial_state)

        response = self._extract_response(
            final_state,
        )

        self._conversation_service.add_assistant_message(
            conversation=conversation,
            content=response,
        )

        return ChatResult(
            conversation=conversation,
            response=response,
        )

    def _get_or_create_conversation(
        self,
        *,
        user: User,
        conversation_id: UUID | None,
    ) -> Conversation:

        if conversation_id is None:
            return self._conversation_service.create_conversation(
                user=user,
            )

        return self._conversation_service.get_conversation(
            user=user,
            conversation_id=conversation_id,
        )

    def _build_initial_state(
        self,
        *,
        message: str,
    ) -> GraphState:
        return GraphStateFactory.from_user_message(
            message,
        )

    def _extract_response(
        self,
        state: GraphState,
    ) -> str:

        message = state["messages"][-1]

        assert isinstance(message, AIMessage)

        return message.content
