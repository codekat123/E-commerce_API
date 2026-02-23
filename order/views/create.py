from rest_framework.generics import CreateAPIView
from django.db import transaction
from users.permissions import IsClient
from ..serializers import OrderCreateSerializer
from ..models import OrderItem
from cart.service import CartService


class OrderCreateAPIView(CreateAPIView):
    serializer_class = OrderCreateSerializer
    permission_classes = [IsClient]

    def perform_create(self, serializer):
        cart = CartService.checkout(self.request.user)

        with transaction.atomic():
            order = serializer.save(
                customer=self.request.user,
                total_price=cart['total_price']
            )

            order_items = []

            for item in cart['items']:
                product = item['product']

                order_item = OrderItem(
                    order=order,
                    product=product,
                    product_name=product.name,
                    product_price=product.price,
                    quantity=item['quantity'],
                    total_price=product.price * item['quantity']
                )

                order_items.append(order_item)

            OrderItem.objects.bulk_create(order_items)