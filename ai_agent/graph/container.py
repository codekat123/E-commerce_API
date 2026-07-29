from __future__ import annotations

from dataclasses import dataclass

from ai_agent.graph.nodes.chat import ChatNode
from ai_agent.graph.nodes.tool_node import ToolNode
from ai_agent.llm.gemini_client import GeminiClient
from ai_agent.service.tool_executor import ToolExecutor
from ai_agent.tools.order import GetOrderDetailsTool, ListOrdersTool
from ai_agent.tools.registry import ToolRegistry


@dataclass(frozen=True, slots=True)
class GraphContainer:
    chat_node: ChatNode
    tool_node: ToolNode


def build_container() -> GraphContainer:

    tool_registry = ToolRegistry(
        tools=[
            ListOrdersTool(),
            GetOrderDetailsTool(),
        ],
    )

    gemini_client = GeminiClient(tool_registry=tool_registry)

    tool_executor = ToolExecutor(
        tool_registry=tool_registry,
    )

    return GraphContainer(
        chat_node=ChatNode(
            gemini_client=gemini_client,
        ),
        tool_node=ToolNode(
            tool_executor=tool_executor,
        ),
    )
