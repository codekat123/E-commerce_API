from langchain_core.messages import AIMessage

from ai_agent.graph.state import GraphState

TOOL_NODE = "tool"
END_ROUTE = "__end__"


def should_continue(
    state: GraphState,
) -> str:
    last_message = state["messages"][-1]

    if not isinstance(last_message, AIMessage):
        raise ValueError(
            "Expected the last message to be an AIMessage.",
        )

    if last_message.tool_calls:
        return TOOL_NODE

    return END_ROUTE
