from rest_framework.generics import RetrieveAPIView
from ..serializers import OrderDetailSerializer
from ..models import Order


class OrderRetrieveAPIView(RetrieveAPIView):
    serializer_class = OrderDetailSerializer
    lookup_field = "id"

    def get_queryset(self):
        return Order.objects.filter(
            customer=self.request.user
        )