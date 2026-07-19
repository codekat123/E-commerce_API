from __future__ import annotations

from uuid import uuid4

from google.genai import types
from langchain_core.messages import AIMessage


class GeminiResponseParser:
    """
    Converts Gemini SDK responses into LangChain messages.
    """

    def parse(
        self,
        response: types.GenerateContentResponse,
    ) -> AIMessage:
        candidate = self._get_candidate(response)

        content = self._extract_text(candidate)

        tool_calls = self._extract_tool_calls(candidate)

        return AIMessage(
            content=content,
            tool_calls=tool_calls,
        )

    def _get_candidate(
        self,
        response: types.GenerateContentResponse,
    ) -> types.Candidate:
        if not response.candidates:
            raise ValueError("Gemini returned no candidates.")

        return response.candidates[0]

    def _extract_text(
        self,
        candidate: types.Candidate,
    ) -> str:
        texts: list[str] = []

        for part in candidate.content.parts:
            if part.text:
                texts.append(part.text)

        return "\n".join(texts)

    def _extract_tool_calls(
        self,
        candidate: types.Candidate,
    ) -> list[dict]:
        tool_calls: list[dict] = []

        for part in candidate.content.parts:
            function_call = part.function_call

            if function_call is None:
                continue

            tool_calls.append(self._build_tool_call(function_call))

        return tool_calls

    def _build_tool_call(
        self,
        function_call: types.FunctionCall,
    ) -> dict:
        return {
            "id": str(uuid4()),
            "name": function_call.name,
            "args": dict(function_call.args),
        }
