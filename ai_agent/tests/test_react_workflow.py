from __future__ import annotations

from django.contrib.auth import get_user_model
from django.test import TestCase
from langchain_core.messages import (
    AIMessage,
    HumanMessage,
    ToolMessage,
)

from ai_agent.graph.builder import build_graph
from ai_agent.graph.container import GraphContainer
from ai_agent.graph.nodes.chat import ChatNode
from ai_agent.graph.nodes.tool_node import ToolNode
from ai_agent.service.tool_executor import ToolExecutor
from ai_agent.tools.registry import ToolRegistry
from ai_agent.tools.weather import WeatherTool

User = get_user_model()


class FakeGeminiClient:
    def __init__(self) -> None:
        self.calls = 0

    def chat(
        self,
        messages,
    ) -> AIMessage:
        self.calls += 1

        if self.calls == 1:
            return AIMessage(
                content="",
                tool_calls=[
                    {
                        "id": "tool_call_1",
                        "name": "get_weather",
                        "args": {
                            "city": "Cairo",
                        },
                    }
                ],
            )

        return AIMessage(
            content="The weather in Cairo is sunny and 30°C.",
        )


class ReactWorkflowTests(TestCase):
    def setUp(self) -> None:
        self.user = User.objects.create_user(
            email="test@example.com",
            password="password123",
        )

        self.fake_client = FakeGeminiClient()

        tool_registry = ToolRegistry(
            tools=[
                WeatherTool(),
            ],
        )

        container = GraphContainer(
            chat_node=ChatNode(
                gemini_client=self.fake_client,
            ),
            tool_node=ToolNode(
                tool_executor=ToolExecutor(
                    tool_registry=tool_registry,
                ),
            ),
        )

        self.graph = build_graph(
            container=container,
        )

    def test_react_workflow_executes_tool_and_returns_final_answer(self) -> None:
        result = self.graph.invoke(
            {
                "user": self.user,
                "messages": [
                    HumanMessage(
                        content="What's the weather in Cairo?",
                    )
                ],
            }
        )

        messages = result["messages"]

        self.assertEqual(len(messages), 4)

        self.assertIsInstance(
            messages[0],
            HumanMessage,
        )

        self.assertIsInstance(
            messages[1],
            AIMessage,
        )

        self.assertIsInstance(
            messages[2],
            ToolMessage,
        )

        self.assertIsInstance(
            messages[3],
            AIMessage,
        )

        self.assertEqual(
            messages[3].content,
            "The weather in Cairo is sunny and 30°C.",
        )

        self.assertEqual(
            self.fake_client.calls,
            2,
        )
