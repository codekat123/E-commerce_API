from __future__ import annotations

import logging

from google import genai

from ai_agent.llm.config import gemini_config
from ai_agent.llm.exceptions import GeminiEmbeddingError

logger = logging.getLogger(__name__)


class GeminiEmbeddingClient:
    """
    Wrapper around the Google GenAI embedding API.
    """

    def __init__(self) -> None:
        self._client = genai.Client(
            api_key=gemini_config.api_key,
        )

    def embed(
        self,
        text: str,
    ) -> list[float]:
        """
        Generate an embedding vector for the given text.
        """
        if not text.strip():
            raise ValueError("Text cannot be empty.")

        try:
            logger.debug(
                "Generating embedding (length=%d).",
                len(text),
            )

            response = self._client.models.embed_content(
                model=gemini_config.embedding_model,
                contents=text,
            )

            embedding = response.embeddings

            if not embedding:
                raise GeminiEmbeddingError(
                    "Gemini returned no embedding.",
                )

            values = embedding[0].values

            if not values:
                raise GeminiEmbeddingError(
                    "Gemini returned an empty embedding vector.",
                )

            return list(values)

        except GeminiEmbeddingError:
            raise

        except Exception as exc:
            raise GeminiEmbeddingError(
                "Failed to generate embedding.",
            ) from exc
