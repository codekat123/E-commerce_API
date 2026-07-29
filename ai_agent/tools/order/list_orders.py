from __future__ import annotations

from typing import Any

from ai_agent.tools.base import Tool
from ai_agent.tools.schema import (
    ToolDefinition,
    ToolParameter,
    ToolParameterType,
)
from order.models import Order
from users.models import Client


class ListOrdersTool(Tool):
    DEFAULT_LIMIT = 5
    MAX_LIMIT = 20

    @property
    def definition(self) -> ToolDefinition:
        return ToolDefinition(
            name="list_orders",
            description="List the authenticated customer's recent orders.",
            parameters=[
                ToolParameter(
                    name="limit",
                    type=ToolParameterType.INTEGER,
                    description="Maximum number of recent orders to return.",
                    required=False,
                ),
            ],
        )

    def execute(
        self,
        *,
        user,
        arguments: dict[str, Any],
    ) -> dict[str, Any]:
        if not isinstance(user, Client):
            return {
                "success": False,
                "error": "Only clients can list orders.",
            }

        try:
            requested_limit = int(arguments.get("limit", self.DEFAULT_LIMIT))
        except (TypeError, ValueError):
            requested_limit = self.DEFAULT_LIMIT

        limit = max(1, min(requested_limit, self.MAX_LIMIT))

        orders = (
            Order.objects.filter(customer=user)
            .only(
                "id",
                "status",
                "total_price",
                "created_at",
            )
            .order_by("-created_at")[:limit]
        )

        return {
            "success": True,
            "count": len(orders),
            "orders": [
                {
                    "id": order.pk,
                    "status": order.status,
                    "total_price": str(order.total_price),
                    "created_at": order.created_at.isoformat(),
                }
                for order in orders
            ],
        }
