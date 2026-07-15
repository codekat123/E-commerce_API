class GeminiClientError(Exception):
    """Base Gemini exception."""


class GeminiRequestError(GeminiClientError):
    """Gemini request failed."""
