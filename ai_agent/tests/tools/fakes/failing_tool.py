# ai_agent/tests/fakes/failing_tool.py

from __future__ import annotations

from typing import Any

from ai_agent.tests.tools.fakes.fake_tool import FakeTool


class FailingTool(FakeTool):
    def execute(
        self,
        *,
        user,
        arguments: dict[str, Any],
    ) -> dict[str, Any]:
        raise RuntimeError("Boom!")
