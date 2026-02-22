from rest_framework.generics import DestroyAPIView
from rest_framework.permissions import IsAuthenticated
from ..models import Order


class OrderDestroyAPIView(DestroyAPIView):
    permission_classes = [IsAuthenticated]
    lookup_field = "id"

    def get_queryset(self):
        return Order.objects.filter(customer=self.request.user)