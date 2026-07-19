from __future__ import annotations

from django.contrib.auth import get_user_model

from ai_agent.tools.base import Tool

User = get_user_model()


class WeatherTool(Tool):
    """
    Dummy tool used to validate the tool-calling pipeline.
    """

    name = "get_weather"

    description = "Get the current weather for a city."

    def execute(
        self,
        *,
        user: User,
        arguments: dict,
    ) -> dict:
        city = arguments["city"]

        return {
            "city": city,
            "temperature": 30,
            "condition": "Sunny",
        }
