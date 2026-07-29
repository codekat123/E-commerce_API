from __future__ import annotations

from uuid import UUID

from django.contrib.auth import get_user_model
from langchain_core.messages import AIMessage, BaseMessage
from langgraph.graph.state import CompiledStateGraph

from ai_agent.graph.builder import get_graph
from ai_agent.graph.factory import GraphStateFactory
from ai_agent.graph.state import GraphState
from ai_agent.memory.service import MemoryService
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
    - Load conversation context.
    - Execute the AI graph.
    - Persist newly generated graph messages.
    - Return the final assistant response.
    """

    def __init__(
        self,
        *,
        graph: CompiledStateGraph | None = None,
        conversation_service: ConversationService | None = None,
        memory_service: MemoryService | None = None,
        graph_state_factory: GraphStateFactory | None = None,
    ) -> None:
        self._graph: CompiledStateGraph = graph or get_graph()

        self._conversation_service: ConversationService = (
            conversation_service or ConversationService()
        )

        self._memory_service: MemoryService = memory_service or MemoryService()

        self._graph_state_factory: GraphStateFactory = (
            graph_state_factory or GraphStateFactory()
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

        context_messages = self._memory_service.get_context_messages(
            conversation=conversation,
        )

        initial_state = self._build_initial_state(
            user=user,
            messages=context_messages,
        )

        previous_message_count = len(context_messages)

        final_state = self._graph.invoke(initial_state)

        self._persist_new_messages(
            conversation=conversation,
            previous_message_count=previous_message_count,
            state=final_state,
        )

        response = self._extract_response(
            final_state,
        )

        return ChatResult(
            conversation=conversation,
            response=response,
        )

    def _persist_new_messages(
        self,
        *,
        conversation: Conversation,
        previous_message_count: int,
        state: GraphState,
    ) -> None:
        new_messages = state["messages"][previous_message_count:]

        for message in new_messages:
            self._conversation_service.add_langchain_message(
                conversation=conversation,
                message=message,
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
        user: User,
        messages: list[BaseMessage],
    ) -> GraphState:
        return self._graph_state_factory.create(
            messages=messages,
            user=user,
        )

    def _extract_response(
        self,
        state: GraphState,
    ) -> str:
        message = state["messages"][-1]

        assert isinstance(message, AIMessage)

        return message.content
