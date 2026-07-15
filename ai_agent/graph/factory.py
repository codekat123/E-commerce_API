from __future__ import annotations

from langchain_core.messages import HumanMessage

from ai_agent.graph.state import GraphState


class GraphStateFactory:
    """
    Factory responsible for creating valid GraphState instances.
    """

    @staticmethod
    def from_user_message(message: str) -> GraphState:
        """
        Create the initial graph state for a new user message.
        """

        return {
            "messages": [
                HumanMessage(content=message),
            ]
        }
