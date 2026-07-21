from __future__ import annotations

from ai_agent.graph.state import GraphState
from ai_agent.llm.gemini_client import GeminiClient


class ChatNode:
    """
    LangGraph node responsible for generating an AI response.
    """

    def __init__(
        self,
        *,
        gemini_client: GeminiClient,
    ) -> None:
        self._gemini_client = gemini_client

    def __call__(
        self,
        state: GraphState,
    ) -> dict:
        response = self._gemini_client.chat(
            state["messages"],
        )

        return {
            "messages": [response],
        }
