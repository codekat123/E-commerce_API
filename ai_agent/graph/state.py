from __future__ import annotations

from typing import Annotated, Any

from langchain_core.messages import AnyMessage
from langgraph.graph.message import add_messages
from typing_extensions import TypedDict

StateUpdate = dict[str, Any]


class GraphState(TypedDict):
    """
    Shared state flowing through every LangGraph node.

    Each node receives the current state and returns only the
    fields it wants to update. LangGraph merges those updates
    into the existing state.
    """

    messages: Annotated[list[AnyMessage], add_messages]
