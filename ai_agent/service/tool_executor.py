from __future__ import annotations

import logging

from langchain_core.messages import AIMessage, ToolMessage

from ai_agent.tools.registry import ToolRegistry

logger = logging.getLogger(__name__)


class ToolExecutor:
    """Executes tool calls requested by an AIMessage."""

    def __init__(
        self,
        *,
        tool_registry: ToolRegistry,
    ) -> None:
        self._tool_registry = tool_registry

    def execute(
        self,
        *,
        user,
        message: AIMessage,
    ) -> list[ToolMessage]:
        tool_messages: list[ToolMessage] = []

        for tool_call in message.tool_calls:
            tool_name = tool_call["name"]
            tool_call_id = tool_call["id"]
            arguments = tool_call["args"]

            tool = self._tool_registry.get(tool_name)

            if tool is None:
                logger.warning(
                    "Unknown tool requested: %s",
                    tool_name,
                )

                tool_messages.append(
                    ToolMessage(
                        tool_call_id=tool_call_id,
                        content=f"Unknown tool: {tool_name}",
                    ),
                )
                continue

            try:
                result = tool.execute(
                    user=user,
                    arguments=arguments,
                )
            except Exception:
                logger.exception(
                    "Tool '%s' execution failed.",
                    tool_name,
                )

                tool_messages.append(
                    ToolMessage(
                        tool_call_id=tool_call_id,
                        content=f"Tool '{tool_name}' failed to execute.",
                    ),
                )
                continue

            tool_messages.append(
                ToolMessage(
                    tool_call_id=tool_call_id,
                    content=result,
                ),
            )

        return tool_messages
