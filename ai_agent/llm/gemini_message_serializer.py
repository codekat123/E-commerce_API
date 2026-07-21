from __future__ import annotations

from typing import Any

from google.genai import types
from langchain_core.messages import (
    AIMessage,
    AnyMessage,
    HumanMessage,
    SystemMessage,
    ToolMessage,
)


class GeminiMessageSerializer:
    """
    Serializes LangChain messages into Gemini Content objects.
    """

    def serialize(
        self,
        messages: list[AnyMessage],
    ) -> list[types.Content]:
        return [self._serialize_message(message) for message in messages]

    def _serialize_message(
        self,
        message: AnyMessage,
    ) -> types.Content:
        if isinstance(message, HumanMessage):
            return self._serialize_human_message(message)

        if isinstance(message, AIMessage):
            return self._serialize_ai_message(message)

        if isinstance(message, SystemMessage):
            return self._serialize_system_message(message)

        if isinstance(message, ToolMessage):
            return self._serialize_tool_message(message)

        raise TypeError(f"Unsupported message type: {type(message)!r}")

    def _serialize_human_message(
        self,
        message: HumanMessage,
    ) -> types.Content:
        return types.Content(
            role="user",
            parts=[
                types.Part.from_text(
                    text=message.content,
                )
            ],
        )

    def _serialize_ai_message(
        self,
        message: AIMessage,
    ) -> types.Content:
        if message.tool_calls:
            return self._serialize_ai_tool_calls(
                message.tool_calls,
            )

        return self._serialize_ai_text(message)

    def _serialize_ai_text(
        self,
        message: AIMessage,
    ) -> types.Content:
        return types.Content(
            role="model",
            parts=[
                types.Part.from_text(
                    text=message.content,
                )
            ],
        )

    def _serialize_ai_tool_calls(
        self,
        tool_calls: list[dict[str, Any]],
    ) -> types.Content:
        return types.Content(
            role="model",
            parts=[self._serialize_tool_call(tool_call) for tool_call in tool_calls],
        )

    def _serialize_tool_call(
        self,
        tool_call: dict[str, Any],
    ) -> types.Part:
        return types.Part.from_function_call(
            name=tool_call["name"],
            args=tool_call["args"],
        )

    def _serialize_system_message(
        self,
        message: SystemMessage,
    ) -> types.Content:
        return types.Content(
            role="user",
            parts=[
                types.Part.from_text(
                    text=message.content,
                )
            ],
        )

    def _serialize_tool_message(
        self,
        message: ToolMessage,
    ) -> types.Content:
        return types.Content(
            role="user",
            parts=[
                types.Part.from_function_response(
                    name=message.name,
                    response={
                        "result": message.content,
                    },
                )
            ],
        )
