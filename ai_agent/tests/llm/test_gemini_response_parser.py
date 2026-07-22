from django.test import TestCase
from google.genai import types
from langchain_core.messages import AIMessage

from ai_agent.llm.parser import GeminiResponseParser


class GeminiResponseParserTests(TestCase):
    def setUp(self) -> None:
        self.parser = GeminiResponseParser()

    def test_parses_text_response(self) -> None:
        response = types.GenerateContentResponse(
            candidates=[
                types.Candidate(
                    content=types.Content(
                        role="model",
                        parts=[
                            types.Part.from_text(
                                text="Hello Ahmed!",
                            ),
                        ],
                    ),
                ),
            ],
        )

        message = self.parser.parse(response)

        self.assertIsInstance(message, AIMessage)
        self.assertEqual(message.content, "Hello Ahmed!")
        self.assertEqual(message.tool_calls, [])

    def test_parses_function_call(self) -> None:
        response = types.GenerateContentResponse(
            candidates=[
                types.Candidate(
                    content=types.Content(
                        role="model",
                        parts=[
                            types.Part.from_function_call(
                                name="get_weather",
                                args={
                                    "city": "Cairo",
                                },
                            ),
                        ],
                    ),
                ),
            ],
        )

        message = self.parser.parse(response)

        self.assertEqual(message.content, "")
        self.assertEqual(len(message.tool_calls), 1)

        tool_call = message.tool_calls[0]

        self.assertTrue(tool_call["id"])
        self.assertEqual(tool_call["name"], "get_weather")
        self.assertEqual(
            tool_call["args"],
            {
                "city": "Cairo",
            },
        )

    def test_parses_text_and_function_call(self) -> None:
        response = types.GenerateContentResponse(
            candidates=[
                types.Candidate(
                    content=types.Content(
                        role="model",
                        parts=[
                            types.Part.from_text(
                                text="Let me check.",
                            ),
                            types.Part.from_function_call(
                                name="get_weather",
                                args={
                                    "city": "Cairo",
                                },
                            ),
                        ],
                    ),
                ),
            ],
        )

        message = self.parser.parse(response)

        self.assertEqual(
            message.content,
            "Let me check.",
        )

        self.assertEqual(len(message.tool_calls), 1)

        self.assertEqual(
            message.tool_calls[0]["name"],
            "get_weather",
        )

        self.assertEqual(
            message.tool_calls[0]["args"],
            {
                "city": "Cairo",
            },
        )

    def test_returns_empty_tool_calls_when_response_contains_only_text(self) -> None:
        response = types.GenerateContentResponse(
            candidates=[
                types.Candidate(
                    content=types.Content(
                        role="model",
                        parts=[
                            types.Part.from_text(
                                text="Only text.",
                            ),
                        ],
                    ),
                ),
            ],
        )

        message = self.parser.parse(response)

        self.assertEqual(message.tool_calls, [])

    def test_raises_error_when_response_has_no_candidates(self) -> None:
        response = types.GenerateContentResponse(
            candidates=[],
        )

        with self.assertRaises(ValueError):
            self.parser.parse(response)
