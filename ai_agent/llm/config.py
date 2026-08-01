from __future__ import annotations

from dataclasses import dataclass

from django.conf import settings


@dataclass(frozen=True, slots=True)
class GeminiConfig:
    """
    Configuration for the Gemini chat model.
    """

    api_key: str
    model: str
    temperature: float
    embedding_model: str


gemini_config = GeminiConfig(
    api_key=settings.GEMINI_API_KEY,
    model="gemini-2.5-flash",
    temperature=0.2,
    embedding_model="gemini-embedding-001",
)
