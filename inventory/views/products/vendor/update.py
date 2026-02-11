from rest_framework.generics import UpdateAPIView
from users.permissions import IsVendor
from ....serializers import ProductVendorUpdateCreateSerializer
from ....models import Product


class ProductUpdateAPIView(UpdateAPIView):
    serializer_class = ProductVendorUpdateCreateSerializer
    permission_classes = [IsVendor]
    lookup_field = 'uuid'

    def get_queryset(self):
        return Product.objects.filter(vendor=self.request.user)
