class GeminiClientError(Exception):
    """Base Gemini exception."""


class GeminiRequestError(GeminiClientError):
    """Gemini request failed."""


class GeminiEmbeddingError(GeminiClientError):
    """Gemini embedding request failed."""
