from __future__ import annotations

from collections.abc import Iterable

from ai_agent.tools.base import Tool
from ai_agent.tools.schema import ToolDefinition


class ToolRegistry:
    """
    Stores and resolves available tools.
    """

    def __init__(
        self,
        *,
        tools: Iterable[Tool],
    ) -> None:
        self._tools: dict[str, Tool] = {}

        for tool in tools:
            tool_name = tool.definition.name

            if tool_name in self._tools:
                raise ValueError(
                    f"Duplicate tool name registered: '{tool_name}'.",
                )

            self._tools[tool_name] = tool

    def get(
        self,
        name: str,
    ) -> Tool | None:
        return self._tools.get(name)

    def definitions(self) -> tuple[ToolDefinition, ...]:
        return tuple(tool.definition for tool in self._tools.values())
