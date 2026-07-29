from typing import Any

from ai_agent.tools.base import Tool
from ai_agent.tools.schema import (
    ToolDefinition,
    ToolParameter,
    ToolParameterType,
)
from order.models import Order
from users.models import Client


class GetOrderDetailsTool(Tool):
    @property
    def definition(self) -> ToolDefinition:
        return ToolDefinition(
            name="get_order_details",
            description=(
                "Retrieve details about a customer's order. "
                "If no order ID is provided, retrieve the customer's latest order."
            ),
            parameters=[
                ToolParameter(
                    name="order_id",
                    type=ToolParameterType.INTEGER,
                    description="The order id.",
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
                "message": "Only clients can get order details.",
            }

        order_id = arguments.get("order_id")

        orders = Order.objects.filter(customer=user).prefetch_related("items")

        if order_id is not None:
            order = orders.filter(id=order_id).first()
        else:
            order = orders.order_by("-created_at").first()

        if not order:
            return {
                "success": False,
                "message": "Order not found.",
            }

        return {
            "success": True,
            "order": {
                "id": order.id,
                "status": order.get_status_display(),
                "total_price": str(order.total_price),
                "created_at": order.created_at.isoformat(),
                "items": [
                    {
                        "name": item.product_name,
                        "price": str(item.product_price),
                        "quantity": item.quantity,
                        "total_price": str(item.total_price),
                    }
                    for item in order.items.all()
                ],
            },
        }
