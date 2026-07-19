from __future__ import annotations

from abc import ABC, abstractmethod
from typing import Any

from django.contrib.auth import get_user_model

User = get_user_model()


class Tool(ABC):
    """
    Base class for all AI tools.
    """

    name: str
    description: str

    @abstractmethod
    def execute(
        self,
        *,
        user: User,
        arguments: dict[str, Any],
    ) -> Any:
        """
        Execute the tool.

        Implementations are responsible for performing any required
        authorization and business logic.
        """
        raise NotImplementedError
