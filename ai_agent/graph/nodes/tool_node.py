from __future__ import annotations

from langchain_core.messages import AIMessage

from ai_agent.graph.state import GraphState
from ai_agent.service.tool_executor import ToolExecutor


class ToolNode:
    def __init__(
        self,
        *,
        tool_executor: ToolExecutor,
    ) -> None:
        self._tool_executor = tool_executor

    def __call__(
        self,
        state: GraphState,
    ) -> GraphState:
        last_message = state["messages"][-1]

        if not isinstance(last_message, AIMessage):
            raise ValueError(
                "Expected the last message to be an AIMessage.",
            )

        tool_messages = self._tool_executor.execute(
            user=state["user"],
            message=last_message,
        )

        return {
            "messages": tool_messages,
        }
