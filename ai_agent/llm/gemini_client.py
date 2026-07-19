from __future__ import annotations

from functools import lru_cache

from google import genai
from google.genai import types
from langchain_core.messages import (
    AIMessage,
    AnyMessage,
    HumanMessage,
    SystemMessage,
)

from ai_agent.llm.config import gemini_config
from ai_agent.llm.exceptions import GeminiRequestError
from ai_agent.llm.parser import GeminiResponseParser


class GeminiClient:
    """
    Wrapper around the Google GenAI SDK.
    """

    def __init__(self, parser: GeminiResponseParser | None = None) -> None:
        self._client = genai.Client(
            api_key=gemini_config.api_key,
        )
        self._parser = parser or GeminiResponseParser()

    def chat(
        self,
        messages: list[AnyMessage],
    ) -> AIMessage:
        try:
            contents = self._convert_messages(messages)

            response = self._generate_content(contents)

            return self._parser.parse(response)

        except Exception as exc:
            raise GeminiRequestError("Failed to generate Gemini response.") from exc

    def _convert_messages(
        self,
        messages: list[AnyMessage],
    ) -> list[types.Content]:
        contents: list[types.Content] = []

        for message in messages:
            if isinstance(message, HumanMessage):
                role = "user"
            elif isinstance(message, AIMessage):
                role = "model"
            elif isinstance(message, SystemMessage):
                role = "user"
            else:
                raise TypeError(f"Unsupported message type: {type(message)!r}")

            contents.append(
                types.Content(
                    role=role,
                    parts=[
                        types.Part.from_text(
                            text=message.content,
                        )
                    ],
                )
            )

        return contents


@lru_cache(maxsize=1)
def get_gemini_client() -> GeminiClient:
    """
    Return a cached Gemini client.
    """
    return GeminiClient()
