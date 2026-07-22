from __future__ import annotations

from functools import lru_cache

from langgraph.graph import END, START, StateGraph
from langgraph.graph.state import CompiledStateGraph

from ai_agent.graph.container import GraphContainer, build_container
from ai_agent.graph.routing import (
    END_ROUTE,
    TOOL_NODE,
    should_continue,
)
from ai_agent.graph.state import GraphState

CHAT_NODE = "chat"


def build_graph(
    *,
    container: GraphContainer | None = None,
) -> CompiledStateGraph:
    container = container or build_container()
    builder = StateGraph(GraphState)

    builder.add_node(
        CHAT_NODE,
        container.chat_node,
    )

    builder.add_node(
        TOOL_NODE,
        container.tool_node,
    )

    builder.add_edge(
        START,
        CHAT_NODE,
    )

    builder.add_conditional_edges(
        CHAT_NODE,
        should_continue,
        {
            TOOL_NODE: TOOL_NODE,
            END_ROUTE: END,
        },
    )

    builder.add_edge(
        TOOL_NODE,
        CHAT_NODE,
    )

    return builder.compile()


@lru_cache(maxsize=1)
def get_graph() -> CompiledStateGraph:
    return build_graph()
