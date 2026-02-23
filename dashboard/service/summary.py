from django.db.models import Sum, F, Count, Q, ExpressionWrapper, DecimalField
from inventory.models import Product
from order.models import OrderItem


class VendorDashboardService:

    @staticmethod
    def get_summary(user):

        product_stats = (
            Product.objects
            .filter(vendor=user)
            .aggregate(
                total_products=Count("id"),
                active_products=Count("id", filter=Q(is_archived=False)),
                archived_products=Count("id", filter=Q(is_archived=True)),
            )
        )


        order_stats = (
            OrderItem.objects
            .filter(product__vendor=user)
            .aggregate(
                total_items_sold=Sum("quantity"),
                total_revenue=Sum(
                    ExpressionWrapper(
                        F("quantity") * F("product_price"),
                        output_field=DecimalField()
                    )
                ),
            )
        )

        return {
            "total_products": product_stats["total_products"] or 0,
            "active_products": product_stats["active_products"] or 0,
            "archived_products": product_stats["archived_products"] or 0,
            "total_items_sold": order_stats["total_items_sold"] or 0,
            "total_revenue": order_stats["total_revenue"] or 0,
        }