from rest_framework.generics import CreateAPIView
from ....serializers import ProductVendorUpdateCreateSerializer
from users.permissions import IsVendor
from ....models import Product


class ProductCreateAPIView(CreateAPIView):
    serializer_class = ProductVendorUpdateCreateSerializer
    permission_classes = [IsVendor]

    def perform_create(self, serializer):
        serializer.save(vendor=self.request.user)
