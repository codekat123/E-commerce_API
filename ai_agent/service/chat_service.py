from __future__ import annotations

from langgraph.graph.state import CompiledStateGraph

from ai_agent.graph.builder import get_graph
from ai_agent.graph.factory import GraphStateFactory
from ai_agent.graph.state import GraphState


class ChatService:
    """
    Application service responsible for interacting with the AI graph.
    """

    def __init__(
        self,
        graph: CompiledStateGraph | None = None,
    ) -> None:
        self._graph = graph or get_graph()

    def chat(self, message: str) -> GraphState:
        """
        Execute the AI graph for a single user message.
        """

        initial_state = GraphStateFactory.from_user_message(message)

        return self._graph.invoke(initial_state)
