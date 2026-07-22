from django.test import TestCase
from langchain_core.messages import (
    AIMessage,
    ToolMessage,
)

from ai_agent.service.tool_executor import ToolExecutor
from ai_agent.tests.tools.fakes.failing_tool import FailingTool
from ai_agent.tests.tools.fakes.fake_tool import FakeTool
from ai_agent.tools.registry import ToolRegistry


class ToolExecutorTests(TestCase):
    def test_execute_single_tool_call(self) -> None:
        executor = ToolExecutor(
            tool_registry=ToolRegistry(
                tools=[FakeTool()],
            ),
        )

        message = AIMessage(
            content="",
            tool_calls=[
                {
                    "id": "call_1",
                    "name": "fake_tool",
                    "args": {
                        "value": "hello",
                    },
                },
            ],
        )

        tool_messages = executor.execute(
            user=object(),
            message=message,
        )

        self.assertEqual(len(tool_messages), 1)

        tool_message = tool_messages[0]

        self.assertIsInstance(tool_message, ToolMessage)
        self.assertEqual(tool_message.tool_call_id, "call_1")
        self.assertIn("hello", tool_message.content)

    def test_execute_multiple_tool_calls(self) -> None:
        executor = ToolExecutor(
            tool_registry=ToolRegistry(
                tools=[
                    FakeTool(name="tool_a"),
                    FakeTool(name="tool_b"),
                ],
            ),
        )

        message = AIMessage(
            content="",
            tool_calls=[
                {
                    "id": "call_1",
                    "name": "tool_a",
                    "args": {"value": "one"},
                },
                {
                    "id": "call_2",
                    "name": "tool_b",
                    "args": {"value": "two"},
                },
            ],
        )

        tool_messages = executor.execute(
            user=object(),
            message=message,
        )

        self.assertEqual(len(tool_messages), 2)

        self.assertEqual(tool_messages[0].tool_call_id, "call_1")
        self.assertEqual(tool_messages[1].tool_call_id, "call_2")

    def test_returns_unknown_tool_message(self) -> None:
        executor = ToolExecutor(
            tool_registry=ToolRegistry(
                tools=[],
            ),
        )

        message = AIMessage(
            content="",
            tool_calls=[
                {
                    "id": "call_1",
                    "name": "missing_tool",
                    "args": {},
                },
            ],
        )

        tool_messages = executor.execute(
            user=object(),
            message=message,
        )

        self.assertEqual(len(tool_messages), 1)

        self.assertEqual(
            tool_messages[0].content,
            "Unknown tool: missing_tool",
        )

    def test_returns_failure_message_when_tool_raises_exception(self) -> None:
        executor = ToolExecutor(
            tool_registry=ToolRegistry(
                tools=[FailingTool()],
            ),
        )

        message = AIMessage(
            content="",
            tool_calls=[
                {
                    "id": "call_1",
                    "name": "fake_tool",
                    "args": {
                        "value": "hello",
                    },
                },
            ],
        )

        tool_messages = executor.execute(
            user=object(),
            message=message,
        )

        self.assertEqual(len(tool_messages), 1)

        self.assertEqual(
            tool_messages[0].content,
            "Tool 'fake_tool' failed to execute.",
        )

    def test_preserves_tool_call_id(self) -> None:
        executor = ToolExecutor(
            tool_registry=ToolRegistry(
                tools=[FakeTool()],
            ),
        )

        message = AIMessage(
            content="",
            tool_calls=[
                {
                    "id": "unique_call_id",
                    "name": "fake_tool",
                    "args": {
                        "value": "hello",
                    },
                },
            ],
        )

        tool_messages = executor.execute(
            user=object(),
            message=message,
        )

        self.assertEqual(
            tool_messages[0].tool_call_id,
            "unique_call_id",
        )
