from __future__ import annotations

from functools import lru_cache

from langgraph.graph import END, START, StateGraph
from langgraph.graph.state import CompiledStateGraph

from ai_agent.graph.nodes.chat import chat_node
from ai_agent.graph.state import GraphState

CHAT_NODE = "chat"


def build_graph() -> CompiledStateGraph:
    """
    Build and compile the AI support graph.
    """

    builder = StateGraph(GraphState)

    builder.add_node(CHAT_NODE, chat_node)

    builder.add_edge(START, CHAT_NODE)
    builder.add_edge(CHAT_NODE, END)

    return builder.compile()


@lru_cache(maxsize=1)
def get_graph() -> CompiledStateGraph:
    """
    Return the compiled graph.

    The graph is compiled only once during the lifetime
    of the Django process.
    """

    return build_graph()
