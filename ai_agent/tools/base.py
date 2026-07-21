from __future__ import annotations

from abc import ABC, abstractmethod
from typing import Any

from ai_agent.tools.schema import ToolDefinition


class Tool(ABC):
    @property
    @abstractmethod
    def definition(self) -> ToolDefinition:
        """
        Provider-agnostic description of this tool.
        """

    @abstractmethod
    def execute(
        self,
        *,
        user,
        arguments: dict[str, Any],
    ) -> str:
        """
        Execute the tool.
        """
