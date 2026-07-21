from __future__ import annotations

from google import genai
from google.genai import types
from langchain_core.messages import (
    AIMessage,
    AnyMessage,
)

from ai_agent.llm.config import gemini_config
from ai_agent.llm.exceptions import GeminiRequestError
from ai_agent.llm.gemini_message_serializer import GeminiMessageSerializer
from ai_agent.llm.parser import GeminiResponseParser
from ai_agent.llm.tool_converter import GeminiToolConverter
from ai_agent.tools.registry import ToolRegistry


class GeminiClient:
    """
    Wrapper around the Google GenAI SDK.
    """

    def __init__(
        self,
        *,
        tool_registry: ToolRegistry,
        parser: GeminiResponseParser | None = None,
    ) -> None:
        self._client = genai.Client(
            api_key=gemini_config.api_key,
        )

        self._parser = parser or GeminiResponseParser()
        self._serializer = GeminiMessageSerializer()

        converter = GeminiToolConverter()

        self._tools = [
            types.Tool(
                function_declarations=converter.convert_many(
                    tool_registry.definitions(),
                ),
            ),
        ]

    def chat(
        self,
        messages: list[AnyMessage],
    ) -> AIMessage:
        try:
            contents = self._serializer.serialize(messages)

            response = self._generate_content(contents)

            return self._parser.parse(response)

        except Exception as exc:
            raise GeminiRequestError("Failed to generate Gemini response.") from exc

    def _generate_content(
        self,
        contents: list[types.Content],
    ):
        return self._client.models.generate_content(
            model=gemini_config.model,
            contents=contents,
            config=types.GenerateContentConfig(
                tools=self._tools,
            ),
        )
