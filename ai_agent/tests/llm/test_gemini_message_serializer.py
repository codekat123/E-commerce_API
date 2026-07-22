from django.test import TestCase
from langchain_core.messages import (
    AIMessage,
    HumanMessage,
    SystemMessage,
    ToolMessage,
)

from ai_agent.llm.gemini_message_serializer import GeminiMessageSerializer


class GeminiMessageSerializerTests(TestCase):
    def setUp(self) -> None:
        self.serializer = GeminiMessageSerializer()

    def test_serializes_human_message(self) -> None:
        result = self.serializer.serialize(
            [
                HumanMessage(
                    content="Hello!",
                )
            ]
        )

        self.assertEqual(len(result), 1)

        content = result[0]

        self.assertEqual(content.role, "user")
        self.assertEqual(content.parts[0].text, "Hello!")

    def test_serializes_system_message(self) -> None:
        result = self.serializer.serialize(
            [
                SystemMessage(
                    content="You are a helpful assistant.",
                )
            ]
        )

        self.assertEqual(len(result), 1)

        content = result[0]

        self.assertEqual(content.role, "user")
        self.assertEqual(
            content.parts[0].text,
            "You are a helpful assistant.",
        )

    def test_serializes_ai_text_message(self) -> None:
        result = self.serializer.serialize(
            [
                AIMessage(
                    content="Hello back!",
                )
            ]
        )

        self.assertEqual(len(result), 1)

        content = result[0]

        self.assertEqual(content.role, "model")
        self.assertEqual(
            content.parts[0].text,
            "Hello back!",
        )

    def test_serializes_ai_tool_calls(self) -> None:
        result = self.serializer.serialize(
            [
                AIMessage(
                    content="",
                    tool_calls=[
                        {
                            "id": "call_1",
                            "name": "get_weather",
                            "args": {
                                "city": "Cairo",
                            },
                        },
                    ],
                )
            ]
        )

        self.assertEqual(len(result), 1)

        content = result[0]

        self.assertEqual(content.role, "model")

        function_call = content.parts[0].function_call

        self.assertEqual(
            function_call.name,
            "get_weather",
        )

        self.assertEqual(
            dict(function_call.args),
            {
                "city": "Cairo",
            },
        )

    def test_serializes_tool_message(self) -> None:
        result = self.serializer.serialize(
            [
                ToolMessage(
                    tool_call_id="call_1",
                    name="get_weather",
                    content="Sunny",
                )
            ]
        )

        self.assertEqual(len(result), 1)

        content = result[0]

        self.assertEqual(content.role, "user")

        function_response = content.parts[0].function_response

        self.assertEqual(
            function_response.name,
            "get_weather",
        )

        self.assertEqual(
            dict(function_response.response),
            {
                "result": "Sunny",
            },
        )

    def test_raises_error_for_unsupported_message(self) -> None:
        class UnsupportedMessage:
            pass

        with self.assertRaises(TypeError):
            self.serializer.serialize(
                [
                    UnsupportedMessage(),
                ]
            )
