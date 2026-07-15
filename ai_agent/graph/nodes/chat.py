from __future__ import annotations

from ai_agent.graph.state import GraphState
from ai_agent.llm.gemini_client import get_gemini_client


def chat_node(state: GraphState) -> dict:
    """
    Generate an AI response using Gemini.
    """

    client = get_gemini_client()

    response = client.chat(state["messages"])

    return {
        "messages": [response],
    }
