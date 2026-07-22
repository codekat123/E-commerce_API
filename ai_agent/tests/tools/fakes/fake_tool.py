from __future__ import annotations

from typing import Any

from ai_agent.tools.base import Tool
from ai_agent.tools.schema import (
    ToolDefinition,
    ToolParameter,
    ToolParameterType,
)


class FakeTool(Tool):
    def __init__(
        self,
        *,
        name: str = "fake_tool",
    ) -> None:
        self._definition = ToolDefinition(
            name=name,
            description="Fake tool used for tests.",
            parameters=[
                ToolParameter(
                    name="value",
                    type=ToolParameterType.STRING,
                    description="Dummy value.",
                    required=True,
                ),
            ],
        )

    @property
    def definition(self) -> ToolDefinition:
        return self._definition

    def execute(
        self,
        *,
        user,
        arguments: dict[str, Any],
    ) -> dict[str, Any]:
        return {
            "value": arguments["value"],
        }
